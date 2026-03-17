"""
Rutas para catálogo de pantallas (solo admin)
"""
from flask import Blueprint, render_template, request, redirect, session, url_for, flash, jsonify
from app.models.database import get_db, USE_POSTGRES
from app.utils.decorators import admin_required

pantallas_bp = Blueprint('pantallas', __name__, url_prefix='/pantallas')

PH = '%s' if USE_POSTGRES else '?'


@pantallas_bp.route('/')
@admin_required
def index():
    conn = get_db()
    q = request.args.get('q', '').strip()
    marca = request.args.get('marca', '').strip()

    sql = "SELECT * FROM pantallas"
    params = []
    conds = []
    if q:
        conds.append(f"modelo LIKE {PH}")
        params.append(f'%{q}%')
    if marca:
        conds.append(f"marca = {PH}")
        params.append(marca)
    if conds:
        sql += ' WHERE ' + ' AND '.join(conds)
    sql += ' ORDER BY marca, modelo'

    lista = conn.execute(sql, params).fetchall()
    marcas = [r[0] for r in conn.execute(
        "SELECT DISTINCT marca FROM pantallas ORDER BY marca"
    ).fetchall()]

    return render_template('pantallas.html',
        pantallas=lista, marcas=marcas,
        q=q, marca_sel=marca,
        usuario=session['usuario'], rol=session['rol'])


@pantallas_bp.route('/nueva', methods=['POST'])
@admin_required
def nueva():
    conn = get_db()
    data = _form_data(request)
    conn.execute(f'''
        INSERT INTO pantallas
        (marca, modelo, con_marco, precio_proveedor, anticipo, precio_final,
         precio_publico_1, precio_publico_2)
        VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})
    ''', data)
    conn.commit()
    flash('Pantalla agregada.', 'success')
    return redirect(url_for('pantallas.index'))


@pantallas_bp.route('/editar/<int:pid>', methods=['POST'])
@admin_required
def editar(pid):
    conn = get_db()
    data = _form_data(request)
    data.append(pid)
    conn.execute(f'''
        UPDATE pantallas SET
            marca={PH}, modelo={PH}, con_marco={PH},
            precio_proveedor={PH}, anticipo={PH}, precio_final={PH},
            precio_publico_1={PH}, precio_publico_2={PH}
        WHERE id={PH}
    ''', data)
    conn.commit()
    flash('Pantalla actualizada.', 'success')
    return redirect(url_for('pantallas.index'))


@pantallas_bp.route('/eliminar/<int:pid>', methods=['POST'])
@admin_required
def eliminar(pid):
    conn = get_db()
    conn.execute(f"DELETE FROM pantallas WHERE id={PH}", (pid,))
    conn.commit()
    return redirect(url_for('pantallas.index'))


def _form_data(req):
    marca   = req.form.get('marca', '').strip().upper()
    modelo  = req.form.get('modelo', '').strip().upper()
    con_marco = 1 if req.form.get('con_marco') else 0
    pp  = float(req.form.get('precio_proveedor', 0) or 0)
    ant = float(req.form.get('anticipo', 0) or 0)
    pf  = float(req.form.get('precio_final', 0) or 0)
    p1  = float(req.form.get('precio_publico_1', 0) or 0)
    p2  = float(req.form.get('precio_publico_2', 0) or 0)
    return [marca, modelo, con_marco, pp, ant, pf, p1, p2]
