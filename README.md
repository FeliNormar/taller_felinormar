# ⚙ Taller Felinormar — Sistema de Gestión v2.0

Sistema profesional de gestión para taller de reparación de celulares.  
**Arquitectura Production-Ready** con Factory Pattern y Blueprints.

## 🎯 Características

- ✅ Gestión completa de órdenes de servicio
- ✅ Generación automática de folios (FN-0001, FN-0002...)
- ✅ Dashboard analítico con gráficas (Chart.js)
- ✅ Notificaciones por WhatsApp
- ✅ Códigos QR para equipos
- ✅ Sistema de garantías (30 días)
- ✅ Roles de usuario (Admin/Técnico)
- ✅ Catálogo de reparaciones

---

## 🛠 Stack Tecnológico

### Backend
- **Python 3.11+** - Lenguaje principal
- **Flask 3.x** - Framework web con Factory Pattern
- **SQLite 3** - Base de datos embebida
- **Gunicorn** - Servidor WSGI para producción
- **Werkzeug** - Seguridad (hash de contraseñas)

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

## 📁 Estructura del Proyecto

```
taller_felinormar/
├── app/                        # Aplicación principal
│   ├── __init__.py            # Factory de la aplicación
│   ├── config.py              # Configuraciones por entorno
│   ├── models/
│   │   └── database.py        # Gestión de BD
│   ├── routes/                # Blueprints (rutas)
│   │   ├── auth.py           # Autenticación
│   │   ├── ordenes.py        # Órdenes de servicio
│   │   ├── usuarios.py       # Gestión de usuarios
│   │   ├── reparaciones.py   # Catálogo
│   │   └── dashboard.py      # Analytics
│   └── utils/                 # Utilidades
│       ├── decorators.py     # @login_required, @admin_required
│       └── helpers.py        # Funciones auxiliares
│
├── instance/                   # Base de datos (NO en Git)
│   └── taller_felinormar.db
│
├── static/                     # Archivos estáticos
│   └── uploads/               # Uploads persistentes
│
├── templates/                  # Plantillas HTML (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── index.html
│   ├── nueva_orden.html
│   ├── detalle_orden.html
│   ├── editar_orden.html
│   ├── dashboard.html
│   ├── usuarios.html
│   ├── nuevo_usuario.html
│   └── reparaciones.html
│
├── docs/                       # Documentación
│   ├── DEPLOYMENT.md          # Guía de despliegue
│   ├── CASOS_DE_USO.md        # Casos de uso
│   ├── TECNOLOGIAS.md         # Stack técnico
│   ├── SEGURIDAD.md           # Guía de seguridad
│   └── INICIO_RAPIDO.md       # Quick start
│
├── wsgi.py                    # Entry point WSGI
├── Procfile                   # Config para Render/Railway
├── runtime.txt                # Versión de Python
├── requirements.txt           # Dependencias
├── .env.example               # Ejemplo de variables
└── .gitignore                 # Archivos excluidos
```

---

## 🚀 Instalación Rápida

### 1. Clonar el Repositorio
```bash
git clone <tu-repo-url>
cd taller_felinormar
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar ejemplo
cp .env.example .env

# Generar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Editar .env y pegar la clave generada
```

### 5. Iniciar en Desarrollo
```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

python wsgi.py
```

Accede a: **http://localhost:5000**

**Credenciales por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

⚠️ **Cambia la contraseña en producción**

---

## 🌐 Despliegue a Producción

### Plataformas Soportadas
- ✅ **Render** (Recomendado - Free tier disponible)
- ✅ **Railway** (Fácil despliegue)
- ✅ **VPS** (Ubuntu/Debian con Nginx)
- ✅ **Heroku** (Con Procfile incluido)

### Guía Completa
Ver **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** para instrucciones detalladas de despliegue en cada plataforma.

### Quick Deploy en Render

1. Push a GitHub/GitLab
2. Crear Web Service en Render
3. Configurar variables de entorno:
   ```
   SECRET_KEY=<tu-clave-generada>
   FLASK_ENV=production
   ```
4. Deploy automático

---

## 🔒 Seguridad

### Configuración por Entorno

**Desarrollo:**
- `DEBUG=True`
- `SESSION_COOKIE_SECURE=False` (permite HTTP)
- SECRET_KEY por defecto

**Producción:**
- `DEBUG=False` (automático)
- `SESSION_COOKIE_SECURE=True` (solo HTTPS)
- SECRET_KEY desde variable de entorno (obligatorio)

### Características de Seguridad
- ✅ Contraseñas hasheadas (PBKDF2-SHA256)
- ✅ Sesiones seguras con cookies HttpOnly
- ✅ Protección CSRF integrada
- ✅ SQL injection prevention (consultas parametrizadas)
- ✅ XSS protection (escape automático de Jinja2)
- ✅ Variables de entorno para secretos

Ver **[docs/SEGURIDAD.md](docs/SEGURIDAD.md)** para más detalles.

---

## 📚 Documentación

### Documentación Esencial
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Guía completa de despliegue
- **[CASOS_DE_USO.md](docs/CASOS_DE_USO.md)** - 12 casos de uso detallados
- **[TECNOLOGIAS.md](docs/TECNOLOGIAS.md)** - Stack tecnológico completo
- **[SEGURIDAD.md](docs/SEGURIDAD.md)** - Guía de seguridad
- **[INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md)** - Quick start guide

---

## 🔧 Comandos Útiles

### Desarrollo
```bash
# Iniciar en modo desarrollo
export FLASK_ENV=development
python wsgi.py

# Generar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"
```

### Producción (Local)
```bash
# Con Gunicorn
gunicorn wsgi:app --bind 0.0.0.0:8000 --workers 4
```

### Base de Datos
```bash
# Backup
cp instance/taller_felinormar.db backups/backup_$(date +%Y%m%d).db

# Restaurar
cp backups/backup_YYYYMMDD.db instance/taller_felinormar.db
```

---

## 🎯 Módulos y Funcionalidades

### 1. Gestión de Órdenes
- Folios automáticos (FN-XXXX)
- Datos de cliente y equipo
- Anticipo y saldo pendiente
- Notas internas del técnico

### 2. Estatus del Flujo
| Estatus | Descripción |
|---------|-------------|
| 🔵 Recibido | Equipo ingresado |
| 🟡 En Proceso | Reparación en curso |
| 🟢 Listo | Reparación completada |
| 🟣 Entregado | Equipo entregado |

### 3. Código QR Automático
- Generado al abrir detalle de orden
- Contiene: Folio, Cliente, Equipo
- Botón de impresión

### 4. Notificación WhatsApp
- Botón directo cuando estatus es "Listo"
- Mensaje pre-llenado con costos y saldo

### 5. Garantía Automática
- Se registra al marcar "Entregado"
- Período de 30 días desde entrega

### 6. Dashboard Analítico
- Top 5 modelos más frecuentes
- Reporte financiero (Semana/Mes/Año)
- Distribución por estatus
- KPIs: Total órdenes, Ingresos, Pendientes

### 7. Roles de Usuario
| Rol | Permisos |
|-----|----------|
| **Admin** | Todo: órdenes, dashboard, usuarios, catálogo |
| **Técnico** | Órdenes y dashboard (sin gestión de usuarios) |

---

## 🔄 Diferencias con Versión Anterior

### Mejoras en v2.0

✅ **Arquitectura Profesional**
- Factory Pattern para crear la app
- Blueprints para rutas modulares
- Separación de responsabilidades (MVC)

✅ **Configuración por Entorno**
- Development, Production, Testing
- Variables de entorno
- DEBUG automático según entorno

✅ **Seguridad Mejorada**
- SECRET_KEY obligatoria en producción
- Cookies seguras (HttpOnly, Secure)
- Rutas absolutas para BD

✅ **Production-Ready**
- Gunicorn configurado
- Procfile para plataformas cloud
- Carpeta instance/ para persistencia
- Logs y monitoreo

✅ **Mantenibilidad**
- Código modular y organizado
- Fácil de escalar
- Documentación completa

---

## 🐛 Solución de Problemas

### Error: "No module named 'app'"
```bash
# Asegúrate de estar en el directorio correcto
cd taller_felinormar
python wsgi.py
```

### Error: "SECRET_KEY not configured"
```bash
# Configurar variable de entorno
export SECRET_KEY="tu-clave-aqui"
```

### Error: "Database is locked"
```bash
# Reiniciar la aplicación
# En desarrollo: Ctrl+C y volver a iniciar
# En producción: Reiniciar Gunicorn
```

Ver más en **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md#-solución-de-problemas)**

---

## 📊 Métricas del Proyecto

- **Líneas de código:** ~1,500 (Python + HTML)
- **Archivos:** 25+ archivos organizados
- **Módulos:** 5 blueprints independientes
- **Templates:** 10 plantillas HTML
- **Casos de uso:** 12 documentados

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

---

## 📄 Licencia

[Especifica tu licencia aquí]

---

## 👤 Autor

Taller Felinormar  
Sistema de Gestión de Reparaciones v2.0

---

**Última actualización:** 2026-03-12  
**Versión:** 2.0 (Production-Ready)  
**Python:** 3.11+  
**Flask:** 3.x
