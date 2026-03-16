"""
Rutas de autenticación

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
from flask import Blueprint, render_template, request, redirect, session, url_for, flash, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.database import get_db
import secrets, urllib.request, urllib.error, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Página de inicio de sesión
    
    Implementa limpieza de sesión antes de cada login para evitar
    conflictos con el middleware de verificación.
    """
    # Si ya está logueado, redirigir al dashboard
    if session.get('logged_in'):
        return redirect(url_for('ordenes.index'))
    
    if request.method == 'POST':
        # Limpiar sesión antes de procesar login (seguridad)
        session.clear()
        
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '')
        
        # Validaciones
        if not usuario or not password:
            flash('Usuario y contraseña son obligatorios', 'error')
            return render_template('login.html')
        
        try:
            conn = get_db()
            user = conn.execute(
                "SELECT * FROM usuarios WHERE usuario=?",
                (usuario,)
            ).fetchone()
            
            if user and check_password_hash(user['password'], password):
                # Login exitoso - establecer sesión
                session.clear()  # Limpiar cualquier dato residual
                session['logged_in'] = True
                session['usuario'] = user['usuario']
                session['rol'] = user['rol']
                session.permanent = True  # Hacer la sesión permanente
                
                flash(f'Bienvenido, {user["usuario"]}!', 'success')
                return redirect(url_for('ordenes.index'))
            else:
                flash('Usuario o contraseña incorrectos', 'error')
                
        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')
    
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Cerrar sesión
    
    Limpia completamente la sesión y redirige al login.
    """
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('auth.login'))


def _enviar_email_reset(destino, link):
    """Envía el correo de recuperación usando Brevo API"""
    api_key = current_app.config.get('BREVO_API_KEY')
    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:0 auto;background:#0d0f13;color:#e8ecf4;border-radius:12px;padding:32px;border:1px solid #252a38;">
      <h2 style="color:#00AEEF;font-size:22px;margin-bottom:8px;">🔧 Taller Felinormar</h2>
      <p style="color:#7a8299;font-size:13px;margin-bottom:24px;">Sistema de Gestión</p>
      <p style="margin-bottom:16px;">Recibimos una solicitud para restablecer tu contraseña.</p>
      <p style="margin-bottom:24px;">Haz clic en el botón para crear una nueva contraseña. El enlace expira en <strong>1 hora</strong>.</p>
      <a href="{link}" style="display:inline-block;background:#00AEEF;color:#fff;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:700;font-size:14px;">
        Restablecer contraseña →
      </a>
      <p style="margin-top:24px;font-size:12px;color:#7a8299;">
        Si no solicitaste esto, ignora este correo. Tu contraseña no cambiará.
      </p>
      <hr style="border:none;border-top:1px solid #252a38;margin:24px 0;">
      <p style="font-size:11px;color:#3a3f52;">© 2026 Felipe Norberto Marcelino · Taller Felinormar</p>
    </div>
    """
    payload = json.dumps({
        "sender": {"name": "Taller Felinormar", "email": "isc20350300@gmail.com"},
        "to": [{"email": destino}],
        "subject": "Recuperación de contraseña — Taller Felinormar",
        "htmlContent": html
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.brevo.com/v3/smtp/email',
        data=payload,
        headers={
            'api-key': api_key,
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        raise Exception(f"Brevo {e.code}: {body}")


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Solicitar recuperación de contraseña"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        conn = get_db()
        # Solo buscar admin con ese email
        user = conn.execute(
            "SELECT * FROM usuarios WHERE email=? AND rol='admin'", (email,)
        ).fetchone()

        # Siempre mostrar el mismo mensaje (no revelar si existe o no)
        if user:
            token = secrets.token_urlsafe(32)
            expira = (datetime.utcnow() + timedelta(hours=1)).isoformat()
            conn.execute(
                "INSERT INTO reset_tokens (usuario_id, token, expira) VALUES (?,?,?)",
                (user['id'], token, expira)
            )
            conn.commit()
            link = url_for('auth.reset_password', token=token, _external=True)
            try:
                _enviar_email_reset(email, link)
            except Exception as e:
                current_app.logger.error(f"Error enviando email: {e}")
                flash('Error al enviar el correo. Intenta de nuevo.', 'error')
                return render_template('forgot_password.html')

        flash('Si ese correo está registrado, recibirás un enlace en breve.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Restablecer contraseña con token válido"""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM reset_tokens WHERE token=? AND usado=0", (token,)
    ).fetchone()

    if not row or datetime.utcnow() > datetime.fromisoformat(row['expira']):
        flash('El enlace es inválido o ya expiró.', 'error')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm  = request.form.get('password_confirm', '')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('reset_password.html', token=token)
        if password != confirm:
            flash('Las contraseñas no coinciden.', 'error')
            return render_template('reset_password.html', token=token)

        conn.execute(
            "UPDATE usuarios SET password=? WHERE id=?",
            (generate_password_hash(password), row['usuario_id'])
        )
        conn.execute("UPDATE reset_tokens SET usado=1 WHERE id=?", (row['id'],))
        conn.commit()

        flash('Contraseña actualizada. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)
