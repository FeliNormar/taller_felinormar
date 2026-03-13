"""
Rutas para gestión de usuarios (solo admin)

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash
from app.models.database import get_db
from app.utils.decorators import admin_required

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios_bp.route('/')
@admin_required
def index():
    """Lista de usuarios"""
    conn = get_db()
    lista = conn.execute(
        "SELECT id, usuario, rol FROM usuarios ORDER BY id"
    ).fetchall()
    
    return render_template(
        'usuarios.html',
        usuarios=lista,
        usuario=session['usuario'],
        rol=session['rol']
    )


@usuarios_bp.route('/nuevo', methods=['GET', 'POST'])
@admin_required
def nuevo_usuario():
    """Crear nuevo usuario"""
    from flask import flash
    
    if request.method == 'POST':
        usu = request.form.get('usuario', '').strip()
        pwd = request.form.get('password', '').strip()
        rol = request.form.get('rol', 'tecnico')
        
        # Validaciones
        if not usu or not pwd:
            flash('Usuario y contraseña son obligatorios', 'error')
            return render_template(
                'nuevo_usuario.html',
                usuario=session['usuario'],
                rol=session['rol']
            )
        
        if len(pwd) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template(
                'nuevo_usuario.html',
                usuario=session['usuario'],
                rol=session['rol']
            )
        
        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO usuarios (usuario, password, rol) VALUES (?,?,?)",
                (usu, generate_password_hash(pwd), rol)
            )
            conn.commit()
            flash(f'Usuario "{usu}" creado exitosamente', 'success')
            return redirect(url_for('usuarios.index'))
        except Exception as e:
            flash('El nombre de usuario ya existe', 'error')
            return render_template(
                'nuevo_usuario.html',
                usuario=session['usuario'],
                rol=session['rol']
            )
    
    return render_template(
        'nuevo_usuario.html',
        usuario=session['usuario'],
        rol=session['rol']
    )


@usuarios_bp.route('/eliminar/<int:uid>', methods=['POST'])
@admin_required
def eliminar_usuario(uid):
    """Eliminar un usuario"""
    conn = get_db()
    conn.execute(
        "DELETE FROM usuarios WHERE id=? AND usuario != 'admin'",
        (uid,)
    )
    conn.commit()
    return redirect(url_for('usuarios.index'))
