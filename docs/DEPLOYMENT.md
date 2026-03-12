# 🚀 Guía de Despliegue a Producción

## Estructura del Proyecto (Production-Ready)

```
taller_felinormar/
├── app/                        # Aplicación principal (Factory Pattern)
│   ├── __init__.py            # Factory de la aplicación
│   ├── config.py              # Configuraciones por entorno
│   ├── models/
│   │   └── database.py        # Gestión de base de datos
│   ├── routes/                # Blueprints (rutas separadas)
│   │   ├── auth.py
│   │   ├── ordenes.py
│   │   ├── usuarios.py
│   │   ├── reparaciones.py
│   │   └── dashboard.py
│   └── utils/                 # Utilidades
│       ├── decorators.py      # @login_required, @admin_required
│       └── helpers.py         # Funciones auxiliares
│
├── instance/                   # Base de datos (NO en Git)
│   └── taller_felinormar.db
│
├── static/                     # Archivos estáticos
│   └── uploads/               # Uploads persistentes
│
├── templates/                  # Plantillas HTML
│
├── wsgi.py                    # Entry point WSGI
├── Procfile                   # Configuración para Render/Railway
├── runtime.txt                # Versión de Python
├── requirements.txt           # Dependencias
├── .env.example               # Ejemplo de variables de entorno
└── .gitignore                 # Archivos excluidos
```

---

## 📋 Pre-requisitos

1. **Python 3.11+** instalado
2. **Git** configurado
3. Cuenta en plataforma de despliegue (Render, Railway, o VPS)

---

## 🔧 Configuración Local

### 1. Clonar el Repositorio
```bash
git clone <tu-repo-url>
cd taller_felinormar
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv

# Activar
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
```bash
# Copiar ejemplo
cp .env.example .env

# Editar .env y configurar:
# - SECRET_KEY (generar una nueva)
# - FLASK_ENV=development
```

**Generar SECRET_KEY segura:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Iniciar en Desarrollo
```bash
# Modo desarrollo
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows

python wsgi.py
```

Accede a: http://localhost:5000

---

## 🌐 Despliegue en Render

### 1. Preparar el Repositorio
```bash
git add .
git commit -m "Preparado para producción"
git push origin main
```

### 2. Crear Web Service en Render

1. Ve a [render.com](https://render.com) y crea una cuenta
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub/GitLab
4. Configuración:
   - **Name:** taller-felinormar
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Plan:** Free (o el que prefieras)

### 3. Configurar Variables de Entorno

En Render Dashboard → Environment:

```
SECRET_KEY=<tu-clave-generada-aleatoria>
FLASK_ENV=production
```

### 4. Deploy

Click en "Create Web Service" y espera el despliegue (2-5 minutos).

### 5. Configurar Disco Persistente (Opcional)

Para que la base de datos persista entre deploys:

1. En Render Dashboard → tu servicio → "Disks"
2. Add Disk:
   - **Name:** database
   - **Mount Path:** `/opt/render/project/src/instance`
   - **Size:** 1GB (suficiente)

---

## 🚂 Despliegue en Railway

### 1. Preparar el Repositorio
```bash
git add .
git commit -m "Preparado para producción"
git push origin main
```

### 2. Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app)
2. Click en "New Project" → "Deploy from GitHub repo"
3. Selecciona tu repositorio

### 3. Configurar Variables de Entorno

En Railway Dashboard → Variables:

```
SECRET_KEY=<tu-clave-generada-aleatoria>
FLASK_ENV=production
PORT=5000
```

### 4. Deploy Automático

Railway detecta automáticamente:
- `requirements.txt` → Instala dependencias
- `Procfile` → Usa Gunicorn
- `runtime.txt` → Usa Python 3.11

El despliegue es automático.

### 5. Volumen Persistente

Railway incluye almacenamiento persistente por defecto en `/app/instance`.

---

## 🖥️ Despliegue en VPS (Ubuntu)

### 1. Conectar al VPS
```bash
ssh usuario@tu-servidor.com
```

### 2. Instalar Dependencias del Sistema
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nginx supervisor -y
```

### 3. Clonar el Proyecto
```bash
cd /var/www
sudo git clone <tu-repo-url> taller_felinormar
cd taller_felinormar
```

### 4. Configurar Entorno Virtual
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno
```bash
sudo nano /var/www/taller_felinormar/.env
```

Agregar:
```
SECRET_KEY=<tu-clave-generada>
FLASK_ENV=production
```

### 6. Configurar Gunicorn con Supervisor

Crear archivo de configuración:
```bash
sudo nano /etc/supervisor/conf.d/taller_felinormar.conf
```

Contenido:
```ini
[program:taller_felinormar]
directory=/var/www/taller_felinormar
command=/var/www/taller_felinormar/venv/bin/gunicorn wsgi:app --bind 127.0.0.1:8000 --workers 4
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/taller_felinormar/err.log
stdout_logfile=/var/log/taller_felinormar/out.log
```

Crear carpeta de logs:
```bash
sudo mkdir -p /var/log/taller_felinormar
sudo chown www-data:www-data /var/log/taller_felinormar
```

Iniciar servicio:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start taller_felinormar
```

### 7. Configurar Nginx

Crear configuración:
```bash
sudo nano /etc/nginx/sites-available/taller_felinormar
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/taller_felinormar/static;
        expires 30d;
    }
}
```

Activar sitio:
```bash
sudo ln -s /etc/nginx/sites-available/taller_felinormar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Configurar SSL con Let's Encrypt (Opcional)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com
```

---

## 🔒 Seguridad en Producción

### Checklist de Seguridad

- [ ] `SECRET_KEY` generada aleatoriamente
- [ ] `DEBUG=False` en producción
- [ ] Variables de entorno configuradas (no hardcodeadas)
- [ ] Base de datos fuera del repositorio Git
- [ ] HTTPS configurado (SSL/TLS)
- [ ] Firewall configurado (solo puertos 80, 443, 22)
- [ ] Contraseña de admin cambiada
- [ ] Backups automáticos configurados

### Generar SECRET_KEY Segura
```python
import secrets
print(secrets.token_hex(32))
```

### Cambiar Contraseña de Admin

1. Accede a la aplicación
2. Ve a Usuarios → Nuevo Usuario
3. Crea un nuevo admin con contraseña segura
4. Elimina el usuario admin original

---

## 📊 Monitoreo y Logs

### Ver Logs en Render
```
Render Dashboard → tu servicio → Logs
```

### Ver Logs en Railway
```
Railway Dashboard → tu proyecto → Deployments → View Logs
```

### Ver Logs en VPS
```bash
# Logs de Gunicorn
sudo tail -f /var/log/taller_felinormar/out.log
sudo tail -f /var/log/taller_felinormar/err.log

# Logs de Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs de Supervisor
sudo tail -f /var/log/supervisor/supervisord.log
```

---

## 🔄 Actualizar la Aplicación

### En Render/Railway
```bash
git add .
git commit -m "Actualización"
git push origin main
```
El despliegue es automático.

### En VPS
```bash
cd /var/www/taller_felinormar
sudo git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart taller_felinormar
```

---

## 💾 Backups

### Backup Manual de Base de Datos
```bash
# Copiar archivo
cp instance/taller_felinormar.db backups/backup_$(date +%Y%m%d).db
```

### Backup Automático (Cron en VPS)
```bash
# Editar crontab
crontab -e

# Agregar (backup diario a las 2 AM)
0 2 * * * cp /var/www/taller_felinormar/instance/taller_felinormar.db /var/backups/taller_$(date +\%Y\%m\%d).db
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'app'"
```bash
# Asegúrate de estar en el directorio correcto
cd /ruta/a/taller_felinormar
python wsgi.py
```

### Error: "Database is locked"
```bash
# Reiniciar Gunicorn
sudo supervisorctl restart taller_felinormar
```

### Error: "SECRET_KEY not configured"
```bash
# Verificar variables de entorno
echo $SECRET_KEY

# Si está vacía, configurarla
export SECRET_KEY="tu-clave-aqui"
```

### Error 502 Bad Gateway (Nginx)
```bash
# Verificar que Gunicorn esté corriendo
sudo supervisorctl status taller_felinormar

# Si no está corriendo, iniciarlo
sudo supervisorctl start taller_felinormar
```

---

## 📞 Soporte

- **Documentación:** `docs/README.md`
- **Casos de Uso:** `docs/CASOS_DE_USO.md`
- **Tecnologías:** `docs/TECNOLOGIAS.md`
- **Seguridad:** `docs/SEGURIDAD.md`

---

**Última actualización:** 2026-03-12  
**Versión:** 2.0 (Production-Ready)
