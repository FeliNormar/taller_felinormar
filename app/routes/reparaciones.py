"""
Rutas para gestión del catálogo de reparaciones (solo admin)

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, redirect, session, url_for
from app.models.database import get_db
from app.utils.decorators import admin_required

reparaciones_bp = Blueprint('reparaciones', __name__, url_prefix='/reparaciones')


@reparaciones_bp.route('/')
@admin_required
def index():
    """Lista de reparaciones"""
    conn = get_db()
    lista = conn.execute(
        "SELECT * FROM reparaciones ORDER BY descripcion"
    ).fetchall()
    
    return render_template(
        'reparaciones.html',
        reparaciones=lista,
        usuario=session['usuario'],
        rol=session['rol']
    )


@reparaciones_bp.route('/nueva', methods=['POST'])
@admin_required
def nueva_reparacion():
    """Crear nueva reparación"""
    desc = request.form['descripcion'].strip()
    costo = float(request.form.get('costo', 0) or 0)
    
    conn = get_db()
    conn.execute(
        "INSERT INTO reparaciones (descripcion, costo) VALUES (?,?)",
        (desc, costo)
    )
    conn.commit()
    
    return redirect(url_for('reparaciones.index'))


@reparaciones_bp.route('/eliminar/<int:rid>', methods=['POST'])
@admin_required
def eliminar_reparacion(rid):
    """Eliminar una reparación"""
    conn = get_db()
    conn.execute("DELETE FROM reparaciones WHERE id=?", (rid,))
    conn.commit()
    return redirect(url_for('reparaciones.index'))
