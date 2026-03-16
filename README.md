# Taller Felinormar — Sistema de Gestión v2.1

Sistema profesional de gestión para taller de reparación de celulares.

## Características

- Gestión completa de órdenes de servicio
- Folios automáticos (FN-0001, FN-0002...)
- Dashboard analítico con gráficas (Chart.js)
- Notificaciones por WhatsApp
- Códigos QR para equipos
- Sistema de garantías (30 días)
- Roles de usuario (Admin/Técnico)
- Catálogo de reparaciones
- Evidencia fotográfica por orden (upload + cámara, hasta 16 MB)
- Recuperación de contraseña por correo (Brevo API)
- Onboarding de datos del taller al primer arranque
- Página de configuración editable desde el sistema
- Página pública de estatus para clientes

---

## Stack Tecnológico

- **Python 3.11+** + **Flask 3.x** — Backend
- **PostgreSQL** — Base de datos en producción (Render)
- **SQLite** — Base de datos en desarrollo local
- **Gunicorn** — Servidor WSGI
- **Brevo API** — Envío de correos transaccionales
- **Chart.js** — Gráficas en dashboard

---

## Estructura del Proyecto

```
taller_felinormar/
├── app/
│   ├── __init__.py            # Factory + rutas setup/onboarding
│   ├── config.py              # Configuración por entorno
│   ├── models/database.py     # BD (PostgreSQL/SQLite automático)
│   └── routes/
│       ├── auth.py            # Login + recuperación de contraseña
│       ├── ordenes.py         # Órdenes + evidencia fotográfica
│       ├── usuarios.py        # Gestión de usuarios
│       ├── reparaciones.py    # Catálogo
│       └── dashboard.py       # Analytics + configuración del taller
├── templates/
│   ├── setup.html             # Instalación inicial
│   ├── onboarding.html        # Datos del taller (primer arranque)
│   ├── configuracion.html     # Editar datos del taller
│   ├── forgot_password.html   # Recuperar contraseña
│   ├── reset_password.html    # Nueva contraseña con token
│   ├── login.html
│   ├── index.html             # Lista de órdenes
│   ├── nueva_orden.html
│   ├── detalle_orden.html     # Incluye evidencia fotográfica
│   ├── editar_orden.html
│   ├── dashboard.html
│   ├── usuarios.html
│   ├── nuevo_usuario.html
│   ├── reparaciones.html
│   └── status_publico.html    # Página pública para clientes
├── static/images/logo.png
├── wsgi.py
├── Procfile
├── requirements.txt
└── .env.example
```

---

## Instalación Local (Desarrollo)

```bash
git clone https://github.com/FeliNormar/taller_felinormar
cd taller_felinormar

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

set FLASK_ENV=development
python wsgi.py
```

Accede a `http://localhost:5000` — te llevará al setup automáticamente.  
En local usa SQLite, no necesitas configurar nada de base de datos.

---

## Despliegue en Render

### 1. Crear la base de datos PostgreSQL
- En Render → New → PostgreSQL
- Región: Oregon, Plan: Free, versión: 16
- Copiar la **Internal Database URL**

### 2. Crear el Web Service
- New → Web Service → conectar repo GitHub
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn wsgi:app --workers 2 --bind 0.0.0.0:$PORT`

### 3. Variables de entorno (Environment)

| Variable | Valor |
|----------|-------|
| `SECRET_KEY` | Clave aleatoria segura |
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | Internal URL de PostgreSQL |
| `ADMIN_EMAIL` | Correo del administrador |
| `BREVO_API_KEY` | API Key de Brevo |
| `MAIL_USERNAME` | Mismo correo que ADMIN_EMAIL |

### 4. Primer arranque
Al entrar por primera vez te llevará al setup para crear el admin, luego al onboarding para los datos del taller. Solo se hace una vez.

---

## Flujo de Primer Arranque

1. `/setup` — Crear usuario administrador (nombre, contraseña, email)
2. `/onboarding` — Datos del taller (nombre, dirección, teléfono)
3. `/login` — Iniciar sesión

Los datos del taller se pueden editar después desde **Configuración** en el sidebar.

---

## Base de Datos — Tablas

| Tabla | Descripción |
|-------|-------------|
| `usuarios` | Usuarios del sistema |
| `clientes` | Datos de clientes |
| `ordenes` | Órdenes de servicio |
| `reparaciones` | Catálogo de reparaciones |
| `evidencias` | Fotos por orden |
| `reset_tokens` | Tokens de recuperación de contraseña |
| `configuracion` | Datos del taller |

---

## Roles de Usuario

| Rol | Permisos |
|-----|----------|
| Admin | Todo: órdenes, dashboard, usuarios, catálogo, configuración |
| Técnico | Órdenes y dashboard únicamente |

---

## Seguridad

- Contraseñas hasheadas (PBKDF2-SHA256)
- Sesiones seguras (HttpOnly, Secure en producción)
- SQL injection prevention (consultas parametrizadas)
- Headers de seguridad HTTP en todas las respuestas
- Tokens de recuperación de un solo uso con expiración de 1 hora

---

## Solución de Problemas

**No llega el correo de recuperación**
- Verificar `BREVO_API_KEY` en Render
- Verificar que `ADMIN_EMAIL` coincida exactamente con el email registrado en la BD (minúsculas)

**Error al arrancar localmente**
```bash
# Asegúrate de estar en la carpeta correcta
cd taller_felinormar
python wsgi.py
```

**Resetear BD local para probar el setup**
```bash
del instance\taller_felinormar.db
python wsgi.py
```

---

## Autor

**Felipe Norberto Marcelino**  
Taller Felinormar — Sistema de Gestión de Reparaciones

**Versión:** 2.1 | **Python:** 3.11+ | **Flask:** 3.x
