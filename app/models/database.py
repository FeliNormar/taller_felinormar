"""
Gestión de base de datos — SQLite (local) / PostgreSQL (producción)

Detecta automáticamente DATABASE_URL para usar PostgreSQL en Render,
y SQLite como fallback para desarrollo local.

Desarrollado por: Felipe Norberto Marcelino
Copyright (c) 2026 Felipe Norberto Marcelino. Todos los derechos reservados.
"""
import os
import sqlite3
from flask import current_app, g
from werkzeug.security import generate_password_hash

# ── Detectar motor ────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL', '')
# Render entrega postgres://, psycopg2 necesita postgresql://
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

USE_POSTGRES = bool(DATABASE_URL)


# ── Wrapper de fila para psycopg2 (imita sqlite3.Row) ────────────────────────
class PgRow(dict):
    """Permite acceso por nombre de columna igual que sqlite3.Row"""
    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self.values())[key]
        return super().__getitem__(key)

    def keys(self):
        return super().keys()


class PgCursor:
    """Cursor de psycopg2 con interfaz compatible con sqlite3"""
    def __init__(self, cursor, conn):
        self._cur = cursor
        self._conn = conn

    @property
    def lastrowid(self):
        self._cur.execute("SELECT lastval()")
        return self._cur.fetchone()[0]

    def execute(self, sql, params=()):
        sql = _adapt_sql(sql)
        self._cur.execute(sql, params)
        return self

    def executemany(self, sql, seq):
        sql = _adapt_sql(sql)
        self._cur.executemany(sql, seq)
        return self

    def fetchone(self):
        row = self._cur.fetchone()
        if row is None:
            return None
        cols = [d[0] for d in self._cur.description]
        return PgRow(zip(cols, row))

    def fetchall(self):
        rows = self._cur.fetchall()
        if not rows:
            return []
        cols = [d[0] for d in self._cur.description]
        return [PgRow(zip(cols, r)) for r in rows]

    def __getattr__(self, name):
        return getattr(self._cur, name)


class PgConnection:
    """Conexión psycopg2 con interfaz compatible con sqlite3"""
    def __init__(self, dsn):
        import psycopg2
        self._conn = psycopg2.connect(dsn)
        self._conn.autocommit = False

    def execute(self, sql, params=()):
        cur = self._conn.cursor()
        return PgCursor(cur, self._conn).execute(sql, params)

    def executemany(self, sql, seq):
        cur = self._conn.cursor()
        return PgCursor(cur, self._conn).executemany(sql, seq)

    def cursor(self):
        return PgCursor(self._conn.cursor(), self._conn)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()


def _adapt_sql(sql):
    """Convierte placeholders ? de SQLite a %s de PostgreSQL"""
    if not USE_POSTGRES:
        return sql
    result = []
    in_string = False
    quote_char = None
    i = 0
    while i < len(sql):
        c = sql[i]
        if in_string:
            result.append(c)
            if c == quote_char:
                in_string = False
        elif c in ("'", '"'):
            in_string = True
            quote_char = c
            result.append(c)
        elif c == '?':
            result.append('%s')
        else:
            result.append(c)
        i += 1
    return ''.join(result)


# ── Conexión ──────────────────────────────────────────────────────────────────
def get_db():
    """Obtener conexión a la base de datos (PostgreSQL o SQLite)"""
    if 'db' not in g:
        if USE_POSTGRES:
            g.db = PgConnection(DATABASE_URL)
        else:
            g.db = sqlite3.connect(
                current_app.config['DATABASE_PATH'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ── DDL adaptado ──────────────────────────────────────────────────────────────
def _ddl(sqlite_sql):
    """Adapta DDL de SQLite a PostgreSQL"""
    if not USE_POSTGRES:
        return sqlite_sql
    sql = sqlite_sql
    sql = sql.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
    sql = sql.replace('INTEGER PRIMARY KEY DEFAULT 1', 'INTEGER PRIMARY KEY DEFAULT 1')
    sql = sql.replace('IF NOT EXISTS\n', 'IF NOT EXISTS ')
    return sql


def init_db():
    """Inicializar base de datos con tablas y datos iniciales"""
    db = get_db()

    # ── Crear todas las tablas ────────────────────────────────
    db.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id       SERIAL PRIMARY KEY,
            usuario  TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol      TEXT NOT NULL DEFAULT 'tecnico',
            email    TEXT
        )
    ''' if USE_POSTGRES else '''
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario  TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol      TEXT NOT NULL DEFAULT 'tecnico',
            email    TEXT
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS reset_tokens (
            id         SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL,
            token      TEXT UNIQUE NOT NULL,
            expira     TEXT NOT NULL,
            usado      INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''' if USE_POSTGRES else '''
        CREATE TABLE IF NOT EXISTS reset_tokens (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            token      TEXT UNIQUE NOT NULL,
            expira     TEXT NOT NULL,
            usado      INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS reparaciones (
            id          SERIAL PRIMARY KEY,
            descripcion TEXT NOT NULL,
            costo       REAL NOT NULL DEFAULT 0
        )
    ''' if USE_POSTGRES else '''
        CREATE TABLE IF NOT EXISTS reparaciones (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            costo       REAL NOT NULL DEFAULT 0
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id       SERIAL PRIMARY KEY,
            nombre   TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''' if USE_POSTGRES else '''
        CREATE TABLE IF NOT EXISTS clientes (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre   TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS ordenes (
            id             SERIAL PRIMARY KEY,
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
    ''' if USE_POSTGRES else '''
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

    db.execute('''
        CREATE TABLE IF NOT EXISTS evidencias (
            id       SERIAL PRIMARY KEY,
            folio    TEXT NOT NULL,
            filename TEXT NOT NULL,
            fecha    TEXT NOT NULL,
            FOREIGN KEY (folio) REFERENCES ordenes(folio)
        )
    ''' if USE_POSTGRES else '''
        CREATE TABLE IF NOT EXISTS evidencias (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            folio    TEXT NOT NULL,
            filename TEXT NOT NULL,
            fecha    TEXT NOT NULL,
            FOREIGN KEY (folio) REFERENCES ordenes(folio)
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS configuracion (
            id                 INTEGER PRIMARY KEY DEFAULT 1,
            nombre_taller      TEXT NOT NULL DEFAULT '',
            nombre_propietario TEXT NOT NULL DEFAULT '',
            email              TEXT NOT NULL DEFAULT '',
            telefono           TEXT NOT NULL DEFAULT '',
            calle              TEXT NOT NULL DEFAULT '',
            colonia            TEXT NOT NULL DEFAULT '',
            municipio          TEXT NOT NULL DEFAULT '',
            estado             TEXT NOT NULL DEFAULT '',
            cp                 TEXT NOT NULL DEFAULT '',
            completado         INTEGER NOT NULL DEFAULT 0
        )
    ''')

    # Commit de todas las tablas antes de cualquier DML
    db.commit()

    # Migración: agregar columna email si no existe (BD existentes)
    try:
        db.execute("ALTER TABLE usuarios ADD COLUMN email TEXT")
        db.commit()
    except Exception:
        if USE_POSTGRES:
            db._conn.rollback()

    # Sincronizar email del admin desde variable de entorno
    admin_email = os.environ.get('ADMIN_EMAIL')
    if admin_email:
        try:
            db.execute(
                "UPDATE usuarios SET email=%s WHERE rol='admin' AND (email IS NULL OR email='')" if USE_POSTGRES
                else "UPDATE usuarios SET email=? WHERE rol='admin' AND (email IS NULL OR email='')",
                (admin_email,)
            )
            db.commit()
        except Exception:
            if USE_POSTGRES:
                db._conn.rollback()

    # Si ya hay usuarios pero no hay configuración, crear una por defecto
    user_count = db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
    cfg_count  = db.execute("SELECT COUNT(*) FROM configuracion").fetchone()[0]
    if user_count > 0 and cfg_count == 0:
        db.execute('''
            INSERT INTO configuracion
            (id, nombre_taller, nombre_propietario, email, telefono,
             calle, colonia, municipio, estado, cp, completado)
            VALUES (1, 'Taller Felinormar', 'Admin', '', '',
                    '', '', 'Nuevo Ixcatlán', 'Veracruz', '', 1)
        ''')
        db.commit()

    # Reparaciones de ejemplo
    count = db.execute("SELECT COUNT(*) FROM reparaciones").fetchone()[0]
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
        db.executemany(
            "INSERT INTO reparaciones (descripcion, costo) VALUES (%s,%s)" if USE_POSTGRES
            else "INSERT INTO reparaciones (descripcion, costo) VALUES (?,?)",
            demos
        )
        db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
