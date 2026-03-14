"""
setup_db.py — Inicializa o migra la base de datos de Taller Felinormar.
Ejecutar ANTES de iniciar la aplicación por primera vez.

    python3 setup_db.py

Si la DB ya existe, este script agrega las columnas/tablas faltantes
sin perder datos existentes.

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_DIR, exist_ok=True)
DB_PATH = os.path.join(INSTANCE_DIR, 'taller_felinormar.db')

def column_exists(conn, table, column):
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r[1] == column for r in rows)

def table_exists(conn, table):
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    return row is not None

def migrate():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    # ── Usuarios ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario  TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol      TEXT NOT NULL DEFAULT 'tecnico'
        )
    ''')
    if not column_exists(conn, 'usuarios', 'rol'):
        c.execute("ALTER TABLE usuarios ADD COLUMN rol TEXT NOT NULL DEFAULT 'tecnico'")
        print("  Migrado: usuarios.rol")

    # ── Reparaciones ─────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS reparaciones (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            costo       REAL NOT NULL DEFAULT 0
        )
    ''')

    # ── Clientes ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre   TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''')

    # ── Órdenes ──────────────────────────────────────────
    # Si la tabla ya existe con el esquema viejo, hacemos ALTER TABLE
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
            notas          TEXT
        )
    ''')

    # Migrar columnas que podrían faltar en la tabla vieja
    migrations_ordenes = [
        ('folio',         'TEXT UNIQUE'),
        ('id_cliente',    'INTEGER'),
        ('imei',          'TEXT'),
        ('reparacion_id', 'INTEGER'),
        ('estatus',       "TEXT NOT NULL DEFAULT 'Recibido'"),
        ('anticipo',      'REAL DEFAULT 0'),
        ('fecha_ingreso', 'TEXT'),
        ('fecha_entrega', 'TEXT'),
        ('tecnico',       'TEXT'),
        ('notas',         'TEXT'),
    ]
    for col, col_type in migrations_ordenes:
        if not column_exists(conn, 'ordenes', col):
            try:
                c.execute(f"ALTER TABLE ordenes ADD COLUMN {col} {col_type}")
                print(f"  Migrado: ordenes.{col}")
            except Exception as e:
                print(f"  Advertencia al migrar {col}: {e}")

    # ── Datos iniciales ───────────────────────────────────
    # Admin
    row = c.execute("SELECT id FROM usuarios WHERE usuario='admin'").fetchone()
    if row is None:
        c.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (?,?,?)",
                  ('admin', generate_password_hash('admin123'), 'admin'))
        print("  Creado usuario admin (contraseña: admin123)")
    else:
        # Actualizar rol a admin si faltaba
        c.execute("UPDATE usuarios SET rol='admin' WHERE usuario='admin'")

    # Reparaciones de ejemplo
    count = c.execute("SELECT COUNT(*) FROM reparaciones").fetchone()[0]
    if count == 0:
        demos = [
            ('Cambio de pantalla',          850),
            ('Cambio de batería',            450),
            ('Reparación de placa',         1200),
            ('Cambio de conector de carga',  350),
            ('Limpieza por humedad',         300),
            ('Cambio de cámara trasera',     600),
            ('Desbloqueo IMEI / cuenta',     400),
            ('Cambio de puerto de audio',    280),
        ]
        c.executemany("INSERT INTO reparaciones (descripcion, costo) VALUES (?,?)", demos)
        print(f"  Agregados {len(demos)} servicios al catálogo")

    conn.commit()
    conn.close()
    print(f"\n✓ Base de datos lista: {os.path.abspath(DB_PATH)}")
    print("  Usuario por defecto → admin / admin123")
    print("  ¡Cambia la contraseña después del primer inicio de sesión!\n")

if __name__ == '__main__':
    print(f"\nInicializando base de datos '{DB_PATH}'...\n")
    migrate()
