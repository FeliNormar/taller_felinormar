"""
Rutas para dashboard analítico

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, session, jsonify, flash, redirect, url_for
from datetime import date, timedelta
from app.models.database import get_db, USE_POSTGRES
from app.utils.decorators import login_required, admin_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Página del dashboard"""
    return render_template(
        'dashboard.html',
        usuario=session['usuario'],
        rol=session['rol']
    )


@dashboard_bp.route('/api/dashboard')
@login_required
def api_dashboard():
    """API REST para datos del dashboard"""
    periodo = request.args.get('periodo', 'mes')
    conn = get_db()

    # Top 5 modelos
    top_modelos = conn.execute('''
        SELECT modelo, COUNT(*) as total
        FROM ordenes
        GROUP BY modelo
        ORDER BY total DESC
        LIMIT 5
    ''').fetchall()

    # Ingresos filtrados por período
    hoy = date.today()
    
    ph = '%s' if USE_POSTGRES else '?'  # placeholder según motor

    if periodo == 'semana':
        lunes = hoy - timedelta(days=hoy.weekday())
        desde = lunes.isoformat()
        query_fin = f'''
            SELECT fecha_ingreso as periodo, SUM(costo_total) as ingreso
            FROM ordenes WHERE fecha_ingreso >= {ph} AND estatus='Entregado'
            GROUP BY fecha_ingreso ORDER BY fecha_ingreso
        '''
        params = (desde,)
    elif periodo == 'ano':
        desde = f'{hoy.year}-01-01'
        if USE_POSTGRES:
            query_fin = f'''
                SELECT TO_CHAR(fecha_ingreso::date, 'MM') as periodo, SUM(costo_total) as ingreso
                FROM ordenes WHERE fecha_ingreso >= {ph} AND estatus='Entregado'
                GROUP BY TO_CHAR(fecha_ingreso::date, 'MM') ORDER BY periodo
            '''
        else:
            query_fin = f'''
                SELECT strftime('%m', fecha_ingreso) as periodo, SUM(costo_total) as ingreso
                FROM ordenes WHERE fecha_ingreso >= {ph} AND estatus='Entregado'
                GROUP BY strftime('%m', fecha_ingreso) ORDER BY periodo
            '''
        params = (desde,)
    else:  # mes
        desde = f'{hoy.year}-{hoy.month:02d}-01'
        query_fin = f'''
            SELECT fecha_ingreso as periodo, SUM(costo_total) as ingreso
            FROM ordenes WHERE fecha_ingreso >= {ph} AND estatus='Entregado'
            GROUP BY fecha_ingreso ORDER BY fecha_ingreso
        '''
        params = (desde,)

    ingresos = conn.execute(query_fin, params).fetchall()

    # Distribución por estatus
    estatus_rows = conn.execute('''
        SELECT estatus, COUNT(*) as total FROM ordenes GROUP BY estatus
    ''').fetchall()

    # Totales generales
    totales = conn.execute('''
        SELECT COUNT(*) as total_ordenes,
               SUM(CASE WHEN estatus='Entregado' THEN costo_total ELSE 0 END) as ingresos_total,
               SUM(CASE WHEN estatus NOT IN ('Entregado') THEN 1 ELSE 0 END) as pendientes
        FROM ordenes
    ''').fetchone()

    return jsonify({
        'top_modelos': [
            {'modelo': r['modelo'], 'total': r['total']} 
            for r in top_modelos
        ],
        'ingresos': [
            {'periodo': r['periodo'], 'ingreso': r['ingreso'] or 0} 
            for r in ingresos
        ],
        'estatus': [
            {'estatus': r['estatus'], 'total': r['total']} 
            for r in estatus_rows
        ],
        'totales': {
            'ordenes': totales['total_ordenes'] or 0,
            'ingresos': totales['ingresos_total'] or 0,
            'pendientes': totales['pendientes'] or 0,
        }
    })


@dashboard_bp.route('/configuracion', methods=['GET', 'POST'])
@admin_required
def configuracion():
    """Editar datos del taller"""
    conn = get_db()
    cfg = conn.execute("SELECT * FROM configuracion WHERE id=1").fetchone()

    if request.method == 'POST':
        nombre_taller      = request.form.get('nombre_taller', '').strip()
        nombre_propietario = request.form.get('nombre_propietario', '').strip()
        email              = request.form.get('email', '').strip()
        telefono           = request.form.get('telefono', '').strip()
        calle              = request.form.get('calle', '').strip()
        colonia            = request.form.get('colonia', '').strip()
        municipio          = request.form.get('municipio', '').strip()
        estado             = request.form.get('estado', '').strip()
        cp                 = request.form.get('cp', '').strip()

        if not all([nombre_taller, nombre_propietario, calle, municipio, estado, cp]):
            flash('Completa todos los campos obligatorios.', 'error')
        else:
            from app.models.database import USE_POSTGRES
            if USE_POSTGRES:
                conn.execute('''
                    INSERT INTO configuracion
                    (id, nombre_taller, nombre_propietario, email, telefono,
                     calle, colonia, municipio, estado, cp, completado)
                    VALUES (1, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
                    ON CONFLICT (id) DO UPDATE SET
                        nombre_taller=%s, nombre_propietario=%s, email=%s,
                        telefono=%s, calle=%s, colonia=%s, municipio=%s,
                        estado=%s, cp=%s, completado=1
                ''', (nombre_taller, nombre_propietario, email, telefono,
                      calle, colonia, municipio, estado, cp,
                      nombre_taller, nombre_propietario, email, telefono,
                      calle, colonia, municipio, estado, cp))
            else:
                conn.execute('''
                    INSERT OR REPLACE INTO configuracion
                    (id, nombre_taller, nombre_propietario, email, telefono,
                     calle, colonia, municipio, estado, cp, completado)
                    VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                ''', (nombre_taller, nombre_propietario, email, telefono,
                      calle, colonia, municipio, estado, cp))
            conn.commit()
            flash('Datos del taller actualizados.', 'success')
            return redirect(url_for('dashboard.configuracion'))

    return render_template(
        'configuracion.html',
        cfg=cfg,
        usuario=session['usuario'],
        rol=session['rol']
    )
