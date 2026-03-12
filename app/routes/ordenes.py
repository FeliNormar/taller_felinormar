"""
Rutas para gestión de órdenes de servicio

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, redirect, session, url_for
from datetime import date
from app.models.database import get_db
from app.utils.decorators import login_required
from app.utils.helpers import generar_folio, whatsapp_link

ordenes_bp = Blueprint('ordenes', __name__)


@ordenes_bp.route('/')
@login_required
def index():
    """Dashboard principal con lista de órdenes"""
    filtro = request.args.get('filtro', 'Todos')
    busqueda = request.args.get('q', '').strip()
    conn = get_db()

    query = '''
        SELECT o.*, c.nombre AS nombre_cliente, c.telefono AS tel_cliente
        FROM ordenes o
        LEFT JOIN clientes c ON o.id_cliente = c.id
    '''
    params = []
    conds = []

    if filtro != 'Todos':
        conds.append("o.estatus = ?")
        params.append(filtro)
    
    if busqueda:
        conds.append("(o.folio LIKE ? OR c.nombre LIKE ? OR o.modelo LIKE ?)")
        params += [f'%{busqueda}%'] * 3

    if conds:
        query += ' WHERE ' + ' AND '.join(conds)
    query += ' ORDER BY o.id DESC'

    ordenes = conn.execute(query, params).fetchall()

    # Contadores de estatus
    stats = {
        row['estatus']: row['total'] 
        for row in conn.execute(
            "SELECT estatus, COUNT(*) as total FROM ordenes GROUP BY estatus"
        ).fetchall()
    }

    return render_template(
        'index.html',
        ordenes=ordenes,
        stats=stats,
        filtro=filtro,
        busqueda=busqueda,
        usuario=session['usuario'],
        rol=session['rol']
    )


@ordenes_bp.route('/nueva_orden', methods=['GET', 'POST'])
@login_required
def nueva_orden():
    """Crear nueva orden de servicio"""
    conn = get_db()
    reparaciones = conn.execute(
        'SELECT * FROM reparaciones ORDER BY descripcion'
    ).fetchall()

    if request.method == 'POST':
        nombre = request.form['nombre_cliente'].strip()
        telefono = request.form['telefono'].strip()
        marca = request.form['marca'].strip()
        modelo = request.form['modelo'].strip()
        imei = request.form.get('imei', '').strip()
        contrasena = request.form.get('contrasena', '').strip()
        problema = request.form['problema'].strip()
        rep_id = request.form.get('reparacion_id') or None
        costo = float(request.form.get('costo_total', 0) or 0)
        anticipo = float(request.form.get('anticipo', 0) or 0)
        notas = request.form.get('notas', '').strip()
        fecha = date.today().isoformat()
        folio = generar_folio()

        # Insertar o recuperar cliente
        cli = conn.execute(
            "SELECT id FROM clientes WHERE telefono=?",
            (telefono,)
        ).fetchone()
        
        if cli:
            id_cliente = cli['id']
        else:
            cur = conn.execute(
                "INSERT INTO clientes (nombre, telefono) VALUES (?,?)",
                (nombre, telefono)
            )
            id_cliente = cur.lastrowid

        conn.execute('''
            INSERT INTO ordenes
            (folio, id_cliente, marca, modelo, imei, contrasena, problema,
             reparacion_id, costo_total, anticipo, fecha_ingreso, tecnico, notas)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (folio, id_cliente, marca, modelo, imei, contrasena, problema,
              rep_id, costo, anticipo, fecha, session['usuario'], notas))
        conn.commit()
        
        return redirect(url_for('ordenes.detalle_orden', folio=folio))

    return render_template(
        'nueva_orden.html',
        reparaciones=reparaciones,
        hoy=date.today().isoformat(),
        usuario=session['usuario'],
        rol=session['rol']
    )


@ordenes_bp.route('/orden/<folio>')
@login_required
def detalle_orden(folio):
    """Ver detalle de una orden"""
    conn = get_db()
    orden = conn.execute('''
        SELECT o.*, c.nombre AS nombre_cliente, c.telefono AS tel_cliente,
               r.descripcion AS desc_reparacion
        FROM ordenes o
        LEFT JOIN clientes c ON o.id_cliente = c.id
        LEFT JOIN reparaciones r ON o.reparacion_id = r.id
        WHERE o.folio = ?
    ''', (folio,)).fetchone()
    
    if not orden:
        return redirect(url_for('ordenes.index'))

    wa_link = None
    garantia = None
    
    if orden['estatus'] == 'Listo':
        wa_link = whatsapp_link(
            orden['tel_cliente'], orden['nombre_cliente'],
            folio, orden['modelo'], orden['costo_total'], orden['anticipo']
        )
    
    if orden['estatus'] == 'Entregado' and orden['fecha_entrega']:
        garantia = f"Su garantía de 30 días inicia a partir del {orden['fecha_entrega']}."

    qr_data = (
        f"Taller Felinormar | Folio: {folio} | "
        f"Cliente: {orden['nombre_cliente']} | "
        f"Equipo: {orden['marca']} {orden['modelo']}"
    )

    return render_template(
        'detalle_orden.html',
        orden=orden,
        wa_link=wa_link,
        garantia=garantia,
        qr_data=qr_data,
        usuario=session['usuario'],
        rol=session['rol']
    )


@ordenes_bp.route('/orden/<folio>/estatus', methods=['POST'])
@login_required
def actualizar_estatus(folio):
    """Actualizar estatus de una orden"""
    nuevo_estatus = request.form['estatus']
    conn = get_db()
    
    if nuevo_estatus == 'Entregado':
        conn.execute(
            "UPDATE ordenes SET estatus=?, fecha_entrega=? WHERE folio=?",
            (nuevo_estatus, date.today().isoformat(), folio)
        )
    else:
        conn.execute(
            "UPDATE ordenes SET estatus=? WHERE folio=?",
            (nuevo_estatus, folio)
        )
    
    conn.commit()
    return redirect(url_for('ordenes.detalle_orden', folio=folio))


@ordenes_bp.route('/orden/<folio>/editar', methods=['GET', 'POST'])
@login_required
def editar_orden(folio):
    """Editar una orden existente"""
    conn = get_db()
    reparaciones = conn.execute(
        'SELECT * FROM reparaciones ORDER BY descripcion'
    ).fetchall()
    
    orden = conn.execute('''
        SELECT o.*, c.nombre AS nombre_cliente, c.telefono AS tel_cliente
        FROM ordenes o LEFT JOIN clientes c ON o.id_cliente = c.id
        WHERE o.folio = ?
    ''', (folio,)).fetchone()
    
    if not orden:
        return redirect(url_for('ordenes.index'))

    if request.method == 'POST':
        marca = request.form['marca'].strip()
        modelo = request.form['modelo'].strip()
        problema = request.form['problema'].strip()
        rep_id = request.form.get('reparacion_id') or None
        costo = float(request.form.get('costo_total', 0) or 0)
        anticipo = float(request.form.get('anticipo', 0) or 0)
        notas = request.form.get('notas', '').strip()
        imei = request.form.get('imei', '').strip()
        contrasena = request.form.get('contrasena', '').strip()

        conn.execute('''
            UPDATE ordenes SET marca=?, modelo=?, problema=?, reparacion_id=?,
            costo_total=?, anticipo=?, notas=?, imei=?, contrasena=?
            WHERE folio=?
        ''', (marca, modelo, problema, rep_id, costo, anticipo, notas, imei, contrasena, folio))
        conn.commit()
        
        return redirect(url_for('ordenes.detalle_orden', folio=folio))

    return render_template(
        'editar_orden.html',
        orden=orden,
        reparaciones=reparaciones,
        usuario=session['usuario'],
        rol=session['rol']
    )
