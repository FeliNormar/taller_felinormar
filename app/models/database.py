"""
Gestión de base de datos SQLite

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import sqlite3
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    """Obtener conexión a la base de datos"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_PATH'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    """Cerrar conexión a la base de datos"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Inicializar base de datos con tablas y datos iniciales"""
    db = get_db()
    c = db.cursor()

    # Tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario  TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol      TEXT NOT NULL DEFAULT 'tecnico',
            email    TEXT
        )
    ''')
    # Agregar columna email si no existe (migración para BD existentes)
    try:
        c.execute("ALTER TABLE usuarios ADD COLUMN email TEXT")
    except Exception:
        pass  # Ya existe

    # Migración: si el admin no tiene email, tomarlo de variable de entorno
    import os
    admin_email = os.environ.get('ADMIN_EMAIL')
    if admin_email:
        c.execute(
            "UPDATE usuarios SET email=? WHERE rol='admin' AND (email IS NULL OR email='')",
            (admin_email,)
        )

    # Tabla de tokens para recuperación de contraseña
    c.execute('''
        CREATE TABLE IF NOT EXISTS reset_tokens (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            token      TEXT UNIQUE NOT NULL,
            expira     TEXT NOT NULL,
            usado      INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # Tabla de reparaciones
    c.execute('''
        CREATE TABLE IF NOT EXISTS reparaciones (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            costo       REAL NOT NULL DEFAULT 0
        )
    ''')

    # Tabla de clientes
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre   TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''')

    # Tabla de órdenes
    c.execute('''
        CREATE TABLE IF NOT EXISTS ordenes (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            folio          TEXT UNIQUE NOT NULL,
            id_cliente     INTEGER,
            marca          TEXT NOT NULL,
            modelo         TEXT NOT NULL,
            imei           TEXT,
            contrasena     TEXT,
            problema       TEXT NOT NULL,
            reparacion_id  INTEGER,
            estatus        TEXT NOT NULL DEFAULT 'Recibido',
            costo_total    REAL DEFAULT 0,
            anticipo       REAL DEFAULT 0,
            fecha_ingreso  TEXT NOT NULL,
            fecha_entrega  TEXT,
            tecnico        TEXT,
            notas          TEXT,
            FOREIGN KEY (id_cliente)    REFERENCES clientes(id),
            FOREIGN KEY (reparacion_id) REFERENCES reparaciones(id)
        )
    ''')

    # Tabla de evidencias fotográficas
    c.execute('''
        CREATE TABLE IF NOT EXISTS evidencias (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            folio    TEXT NOT NULL,
            filename TEXT NOT NULL,
            fecha    TEXT NOT NULL,
            FOREIGN KEY (folio) REFERENCES ordenes(folio)
        )
    ''')

    # NO crear usuario admin por defecto
    # El usuario se crea en la instalación inicial (/setup)

    # Reparaciones de ejemplo
    count = c.execute("SELECT COUNT(*) FROM reparaciones").fetchone()[0]
    if count == 0:
        demos = [
            ('Cambio de pantalla', 850),
            ('Cambio de batería', 450),
            ('Reparación de placa', 1200),
            ('Cambio de conector de carga', 350),
            ('Limpieza por humedad', 300),
            ('Cambio de cámara', 600),
            ('Desbloqueo IMEI', 400),
        ]
        c.executemany(
            "INSERT INTO reparaciones (descripcion, costo) VALUES (?,?)",
            demos
        )

    db.commit()


def init_app(app):
    """Registrar funciones de base de datos con la aplicación"""
    app.teardown_appcontext(close_db)
