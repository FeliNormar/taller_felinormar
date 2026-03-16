#  Taller Felinormar — Sistema de Gestión v2.1

Sistema profesional de gestión para taller de reparación de celulares.  
**Arquitectura Production-Ready** con Factory Pattern y Blueprints.

## Características

-  Gestión completa de órdenes de servicio
-  Generación automática de folios (FN-0001, FN-0002...)
-  Dashboard analítico con gráficas (Chart.js)
-  Notificaciones por WhatsApp
-  Códigos QR para equipos
-  Sistema de garantías (30 días)
-  Roles de usuario (Admin/Técnico)
-  Catálogo de reparaciones
-  Evidencia fotográfica por orden (upload + cámara)
-  Recuperación de contraseña por correo (Brevo API)
-  Onboarding de datos del taller (se pide una sola vez)
-  Página de configuración editable desde el sistema
-  Página pública de estatus para clientes (con fotos y datos del taller)

---

##  Stack Tecnológico

### Backend
- **Python 3.11+** - Lenguaje principal
- **Flask 3.x** - Framework web con Factory Pattern
- **SQLite 3** - Base de datos embebida
- **Gunicorn** - Servidor WSGI para producción
- **Werkzeug** - Seguridad (hash de contraseñas)
- **Brevo API** - Envío de correos transaccionales

### Frontend
- **HTML5 + CSS3** - Estructura y estilos
- **JavaScript Vanilla** - Interactividad
- **Chart.js 4.x** - Visualización de datos
- **QRCode.js** - Generación de códigos QR

### Arquitectura
- **Factory Pattern** - Creación de aplicación Flask
- **Blueprints** - Rutas modulares separadas
- **MVC Pattern** - Separación de responsabilidades
- **Variables de Entorno** - Configuración segura

---

## Estructura del Proyecto

```
taller_felinormar/
├── app/                        # Aplicación principal
│   ├── __init__.py            # Factory de la aplicación + setup/onboarding
│   ├── config.py              # Configuraciones por entorno
│   ├── models/
│   │   └── database.py        # Gestión de BD
│   ├── routes/                # Blueprints (rutas)
│   │   ├── auth.py           # Autenticación + recuperación de contraseña
│   │   ├── ordenes.py        # Órdenes + evidencia fotográfica
│   │   ├── usuarios.py       # Gestión de usuarios
│   │   ├── reparaciones.py   # Catálogo
│   │   └── dashboard.py      # Analytics + configuración del taller
│   └── utils/                 # Utilidades
│       ├── decorators.py     # @login_required, @admin_required
│       └── helpers.py        # Funciones auxiliares
│
├── instance/                   # Base de datos (NO en Git)
│   └── taller_felinormar.db
│
├── static/                     # Archivos estáticos
│   └── uploads/               # Fotos de evidencia (no persistente en Render free)
│
├── templates/                  # Plantillas HTML (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── setup.html             # Instalación inicial
│   ├── onboarding.html        # Datos del taller (primer arranque)
│   ├── configuracion.html     # Editar datos del taller (admin)
│   ├── forgot_password.html   # Solicitar recuperación de contraseña
│   ├── reset_password.html    # Nueva contraseña con token
│   ├── index.html
│   ├── nueva_orden.html
│   ├── detalle_orden.html     # Incluye sección de evidencia fotográfica
│   ├── editar_orden.html
│   ├── dashboard.html
│   ├── usuarios.html
│   ├── nuevo_usuario.html
│   ├── reparaciones.html
│   └── status_publico.html    # Página pública para clientes (con fotos y datos del taller)
│
├── docs/                       # Documentación
│   ├── DEPLOYMENT.md
│   ├── CASOS_DE_USO.md
│   ├── TECNOLOGIAS.md
│   ├── SEGURIDAD.md
│   └── INICIO_RAPIDO.md
│
├── wsgi.py                    # Entry point WSGI
├── Procfile                   # Config para Render/Railway
├── runtime.txt                # Versión de Python
├── requirements.txt           # Dependencias
├── .env.example               # Ejemplo de variables
└── .gitignore
```

---

## Instalación Rápida

### Opción 1: Instalador para Windows (Recomendado)

1. Ve a [Releases](https://github.com/FeliNormar/taller_felinormar/releases)
2. Descarga `TallerFelinormar_v2.1_Setup.exe`
3. Ejecuta el instalador y sigue el asistente
4. El sistema se iniciará automáticamente

**Requisitos:** Windows 10 o superior, Python 3.11+

### Opción 2: Instalación Manual

```bash
git clone https://github.com/FeliNormar/taller_felinormar
cd taller_felinormar

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

pip install -r requirements.txt
```

Configurar variables de entorno (ver sección abajo) y luego:

```bash
set FLASK_ENV=development      # Windows
python wsgi.py
```

Accede a: **http://localhost:5000**

Al primer arranque se mostrará el asistente de configuración.

---

## Variables de Entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `SECRET_KEY` | Clave secreta de Flask | Sí (producción) |
| `FLASK_ENV` | `development` o `production` | Sí |
| `ADMIN_EMAIL` | Email del administrador (para recuperación de contraseña) | Sí |
| `BREVO_API_KEY` | API Key de Brevo para envío de correos | Sí (si usas recuperación de contraseña) |
| `MAIL_USERNAME` | Email remitente (mismo que ADMIN_EMAIL) | Sí |
| `MAIL_PASSWORD` | No requerida con Brevo API | No |

### Ejemplo `.env`
```
SECRET_KEY=tu-clave-secreta-aqui
FLASK_ENV=production
ADMIN_EMAIL=tucorreo@gmail.com
BREVO_API_KEY=xkeysib-...
MAIL_USERNAME=tucorreo@gmail.com
```

---

## Despliegue en Render

1. Push a GitHub
2. Crear Web Service en Render apuntando al repo
3. Configurar las variables de entorno listadas arriba
4. Deploy automático

> **Nota:** En el plan free de Render el disco no es persistente. Las fotos de evidencia se borran al redesplegar. Para persistencia real se requiere un plan paid o almacenamiento externo (S3, Cloudinary).

---

## Flujo de Primer Arranque

1. `/setup` — Crear usuario administrador (usuario, contraseña, email)
2. `/onboarding` — Datos del taller (nombre, dirección, teléfono, etc.)
3. `/login` — Iniciar sesión normalmente

El onboarding solo se muestra una vez. Después se puede editar desde **Configuración** en el sidebar.

---

## Módulos y Funcionalidades

### 1. Gestión de Órdenes
- Folios automáticos (FN-XXXX)
- Datos de cliente y equipo
- Anticipo y saldo pendiente
- Notas internas del técnico

### 2. Evidencia Fotográfica
- Subida de fotos por orden (hasta 16 MB por foto)
- Botón para abrir cámara directamente desde el dispositivo
- Fotos visibles en la página pública del cliente
- Almacenadas en `static/uploads/`

### 3. Recuperación de Contraseña
- Link "¿Olvidaste tu contraseña?" en el login
- Envío de correo con token de un solo uso (expira en 1 hora)
- Implementado con **Brevo API** (no SMTP)
- Solo disponible para el administrador

### 4. Configuración del Taller
- Datos guardados en tabla `configuracion` de la BD
- Editables desde el sidebar → Configuración (solo admin)
- Se muestran en la página pública de estatus del cliente

### 5. Estatus del Flujo
| Estatus | Descripción |
|---------|-------------|
| Recibido | Equipo ingresado |
| En Proceso | Reparación en curso |
| Listo | Reparación completada |
| Entregado | Equipo entregado |

### 6. Código QR Automático
- Generado al abrir detalle de orden
- Contiene: Folio, Cliente, Equipo
- Botón de impresión

### 7. Notificación WhatsApp
- Botón directo cuando estatus es "Listo"
- Mensaje pre-llenado con costos y saldo

### 8. Dashboard Analítico
- Top 5 modelos más frecuentes
- Reporte financiero (Semana/Mes/Año)
- Distribución por estatus
- KPIs: Total órdenes, Ingresos, Pendientes

### 9. Roles de Usuario
| Rol | Permisos |
|-----|----------|
| **Admin** | Todo: órdenes, dashboard, usuarios, catálogo, configuración |
| **Técnico** | Órdenes y dashboard (sin gestión de usuarios ni configuración) |

---

## Base de Datos — Tablas

| Tabla | Descripción |
|-------|-------------|
| `usuarios` | Usuarios del sistema (usuario, password, rol, email) |
| `clientes` | Datos de clientes |
| `ordenes` | Órdenes de servicio |
| `reparaciones` | Catálogo de reparaciones |
| `evidencias` | Fotos por orden (folio, filename, fecha) |
| `reset_tokens` | Tokens de recuperación de contraseña |
| `configuracion` | Datos del taller (nombre, dirección, teléfono, etc.) |

---

## Seguridad

- Contraseñas hasheadas (PBKDF2-SHA256)
- Sesiones seguras con cookies HttpOnly
- SQL injection prevention (consultas parametrizadas)
- XSS protection (escape automático de Jinja2)
- Headers de seguridad HTTP en todas las respuestas
- SECRET_KEY obligatoria en producción
- Tokens de recuperación de un solo uso con expiración

---

## Solución de Problemas

**Error: "No module named 'app'"**
```bash
cd taller_felinormar
python wsgi.py
```

**Error: "SECRET_KEY not configured"**
```bash
export SECRET_KEY="tu-clave-aqui"
```

**No llega el correo de recuperación**
- Verificar que `BREVO_API_KEY` esté configurada en Render
- Verificar que `ADMIN_EMAIL` coincida exactamente con el email registrado en la BD (minúsculas)

**Las fotos desaparecen al redesplegar en Render**
- Es una limitación del plan free (disco efímero)
- Solución: usar plan paid o integrar almacenamiento externo

---

## Autor

**Felipe Norberto Marcelino**  
Taller Felinormar — Sistema de Gestión de Reparaciones

**Última actualización:** 2026-03-15  
**Versión:** 2.1  
**Python:** 3.11+  
**Flask:** 3.x
