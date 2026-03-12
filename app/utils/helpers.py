"""
Funciones auxiliares

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import urllib.parse
from app.models.database import get_db


def generar_folio():
    """Genera el siguiente folio disponible"""
    conn = get_db()
    row = conn.execute(
        "SELECT folio FROM ordenes ORDER BY id DESC LIMIT 1"
    ).fetchone()
    
    if row is None:
        return 'FN-0001'
    
    last = int(row['folio'].split('-')[1])
    return f'FN-{last + 1:04d}'


def whatsapp_link(telefono, nombre, folio, modelo, costo_total, anticipo):
    """Genera enlace de WhatsApp con mensaje pre-llenado"""
    pendiente = costo_total - anticipo
    msg = (
        f"¡Hola {nombre}! 📱 Su equipo *{modelo}* con folio *{folio}* "
        f"ya está listo para recoger en Taller Felinormar. "
        f"Costo total: *${costo_total:.2f}* | Anticipo: *${anticipo:.2f}* | "
        f"Saldo pendiente: *${pendiente:.2f}*. ¡Le esperamos! 🔧"
    )
    phone = '52' + telefono.strip().replace(' ', '').replace('-', '')
    return f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
