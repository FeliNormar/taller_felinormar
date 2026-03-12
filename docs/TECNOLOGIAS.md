# 🛠 Stack Tecnológico - Taller Felinormar

## Resumen Ejecutivo

Sistema web full-stack construido con tecnologías modernas y ligeras, optimizado para talleres de reparación de dispositivos móviles.

---

## 🎯 Arquitectura General

```
┌─────────────────────────────────────────────────────────┐
│                    NAVEGADOR WEB                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   HTML5      │  │    CSS3      │  │  JavaScript  │ │
│  │   Jinja2     │  │  Variables   │  │   Vanilla    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │  Chart.js    │  │  QRCode.js   │                    │
│  │  (Gráficas)  │  │  (Códigos QR)│                    │
│  └──────────────┘  └──────────────┘                    │
└─────────────────────────────────────────────────────────┘
                          ↕ HTTP/HTTPS
┌─────────────────────────────────────────────────────────┐
│                   SERVIDOR FLASK                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Python 3.8+ / Flask 3.1.3           │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │  │
│  │  │   Rutas    │  │  Sesiones  │  │    API     │ │  │
│  │  │ (Routes)   │  │  (Auth)    │  │   REST     │ │  │
│  │  └────────────┘  └────────────┘  └────────────┘ │  │
│  │  ┌────────────┐  ┌────────────┐                 │  │
│  │  │  Werkzeug  │  │   Jinja2   │                 │  │
│  │  │ (Security) │  │ (Templates)│                 │  │
│  │  └────────────┘  └────────────┘                 │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↕ SQL
┌─────────────────────────────────────────────────────────┐
│                   BASE DE DATOS                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │                  SQLite 3                        │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │  │
│  │  │ usuarios │  │ clientes │  │ ordenes  │      │  │
│  │  └──────────┘  └──────────┘  └──────────┘      │  │
│  │  ┌──────────┐                                   │  │
│  │  │reparacion│                                   │  │
│  │  └──────────┘                                   │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Backend

### Python 3.8+
**Versión:** 3.8 o superior  
**Rol:** Lenguaje de programación principal  
**Por qué:** 
- Sintaxis clara y legible
- Amplio ecosistema de librerías
- Excelente para desarrollo web rápido
- Multiplataforma (Windows, Linux, macOS)

### Flask 3.1.3
**Tipo:** Microframework web  
**Rol:** Servidor web y enrutamiento  
**Características usadas:**
- Rutas HTTP (GET, POST)
- Sesiones de usuario
- Templates Jinja2
- Manejo de formularios
- API REST (JSON)

**Ventajas:**
- Ligero y rápido
- Fácil de aprender
- Flexible y extensible
- Ideal para proyectos pequeños/medianos

### SQLite 3
**Tipo:** Base de datos relacional embebida  
**Rol:** Almacenamiento de datos  
**Características:**
- Sin servidor (archivo único)
- ACID compliant
- Soporte de transacciones
- Foreign keys habilitadas

**Ventajas:**
- Cero configuración
- Portátil (un solo archivo .db)
- Rápida para aplicaciones pequeñas
- Respaldos simples (copiar archivo)

**Esquema de Base de Datos:**
```sql
usuarios
├── id (PK)
├── usuario (UNIQUE)
├── password (HASHED)
└── rol (admin/tecnico)

clientes
├── id (PK)
├── nombre
└── telefono

ordenes
├── id (PK)
├── folio (UNIQUE)
├── id_cliente (FK)
├── marca
├── modelo
├── imei
├── contrasena
├── problema
├── reparacion_id (FK)
├── estatus
├── costo_total
├── anticipo
├── fecha_ingreso
├── fecha_entrega
├── tecnico
└── notas

reparaciones
├── id (PK)
├── descripcion
└── costo
```

### Werkzeug
**Tipo:** Librería WSGI  
**Rol:** Seguridad y utilidades  
**Características usadas:**
- `generate_password_hash()` - Hash de contraseñas
- `check_password_hash()` - Verificación de contraseñas
- Algoritmo: PBKDF2-SHA256 con salt

**Seguridad:**
- Las contraseñas NUNCA se almacenan en texto plano
- Hash irreversible con salt único por contraseña
- Protección contra ataques de fuerza bruta

---

## 🎨 Frontend

### HTML5
**Rol:** Estructura de páginas  
**Características usadas:**
- Semántica moderna
- Formularios con validación
- Atributos data-* para JavaScript
- Meta tags responsive

### CSS3
**Rol:** Estilos y diseño visual  
**Técnicas implementadas:**
- **Variables CSS** (`:root`) para tema consistente
- **Flexbox** para layouts flexibles
- **Grid** para estructuras complejas
- **Transiciones** para animaciones suaves
- **Media queries** para responsive design

**Paleta de Colores:**
```css
--bg:       #0d0f13  /* Fondo oscuro */
--surface:  #14171e  /* Superficies */
--panel:    #1c2030  /* Paneles */
--border:   #252a38  /* Bordes */
--amber:    #f5a623  /* Color principal */
--green:    #2ecc71  /* Éxito */
--red:      #e74c3c  /* Error */
--blue:     #3b82f6  /* Info */
--purple:   #a855f7  /* Especial */
--text:     #e8ecf4  /* Texto principal */
--muted:    #7a8299  /* Texto secundario */
```

### JavaScript (Vanilla)
**Rol:** Interactividad del cliente  
**Características:**
- Sin frameworks (JavaScript puro)
- Manipulación del DOM
- Fetch API para llamadas AJAX
- Event listeners
- LocalStorage (si se necesita)

**Ventajas:**
- Sin dependencias adicionales
- Carga rápida
- Fácil mantenimiento
- Compatible con todos los navegadores modernos

### Chart.js 4.x
**Tipo:** Librería de visualización  
**Rol:** Gráficas del dashboard  
**Gráficas implementadas:**
- **Barras horizontales** - Top 5 modelos
- **Línea** - Ingresos por período
- **Dona** - Distribución por estatus

**Configuración:**
```javascript
// Ejemplo: Gráfica de barras
new Chart(ctx, {
  type: 'bar',
  data: { ... },
  options: {
    responsive: true,
    plugins: { legend: { display: false } }
  }
});
```

### QRCode.js
**Tipo:** Generador de códigos QR  
**Rol:** Etiquetas de equipos  
**Características:**
- Generación en el navegador
- Sin servidor necesario
- Personalizable (tamaño, color)
- Imprimible

**Uso:**
```javascript
new QRCode(element, {
  text: "Taller Felinormar | Folio: FN-0001",
  width: 200,
  height: 200
});
```

### Google Fonts
**Tipografías usadas:**
- **Syne** (700, 800) - Títulos y marca
- **DM Mono** (400, 500) - Códigos y datos técnicos
- **Inter** (300, 400, 500) - Texto general

---

## 🏗 Arquitectura y Patrones

### Patrón MVC (Model-View-Controller)

**Model (Modelo):**
- Funciones de acceso a datos (`get_db()`)
- Consultas SQL parametrizadas
- Lógica de negocio (generación de folios, cálculos)

**View (Vista):**
- Templates Jinja2 en carpeta `templates/`
- Herencia de templates (`base.html`)
- Componentes reutilizables

**Controller (Controlador):**
- Rutas Flask (`@app.route()`)
- Validación de entrada
- Lógica de presentación
- Redirecciones

### Jinja2 Templates
**Características usadas:**
- **Herencia** - `{% extends 'base.html' %}`
- **Bloques** - `{% block content %}`
- **Condicionales** - `{% if usuario %}`
- **Loops** - `{% for orden in ordenes %}`
- **Filtros** - `{{ "%.2f"|format(costo) }}`
- **Variables** - `{{ usuario }}`

**Estructura:**
```
base.html (Layout principal)
├── login.html (Sin herencia)
├── index.html
├── nueva_orden.html
├── detalle_orden.html
├── editar_orden.html
├── dashboard.html
├── usuarios.html
├── nuevo_usuario.html
└── reparaciones.html
```

### API REST
**Endpoints JSON:**
```
GET /api/dashboard?periodo=mes
Response: {
  "top_modelos": [...],
  "ingresos": [...],
  "estatus": [...],
  "totales": {...}
}
```

---

## 🔐 Seguridad

### Autenticación
- **Session-based** - Sesiones de Flask
- **Cookies seguras** - HttpOnly, Secure (en HTTPS)
- **Secret key** - Firma de sesiones

### Autorización
- **Decoradores** - `@login_required`, `@admin_required`
- **Roles** - Admin y Técnico
- **Permisos granulares** por ruta

### Protección de Datos
- **Password hashing** - PBKDF2-SHA256
- **SQL injection prevention** - Consultas parametrizadas
- **XSS prevention** - Escape automático de Jinja2
- **CSRF protection** - Token de sesión

**Ejemplo de consulta segura:**
```python
# ✅ SEGURO (parametrizado)
conn.execute("SELECT * FROM usuarios WHERE usuario=?", (usuario,))

# ❌ INSEGURO (concatenación)
conn.execute(f"SELECT * FROM usuarios WHERE usuario='{usuario}'")
```

---

## 🔌 Integraciones

### WhatsApp Business API
**Tipo:** Integración externa  
**Método:** URL Scheme  
**Formato:**
```
https://wa.me/52XXXXXXXXXX?text=Mensaje
```

**Características:**
- Mensaje pre-llenado
- Abre WhatsApp Web o App
- Compatible con móviles y desktop

### Códigos QR
**Contenido:**
```
Taller Felinormar
Folio: FN-0001
Cliente: Juan Pérez
Equipo: Samsung Galaxy S21
```

**Uso:**
- Etiquetas físicas en equipos
- Identificación rápida
- Trazabilidad

---

## 📦 Dependencias

### requirements.txt
```
Flask>=3.0.0
Werkzeug>=3.0.0
```

**Dependencias indirectas:**
- Jinja2 (incluida con Flask)
- Click (incluida con Flask)
- ItsDangerous (incluida con Flask)
- MarkupSafe (incluida con Jinja2)

### CDN (Frontend)
```html
<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>

<!-- QRCode.js -->
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap">
```

---

## 🚀 Despliegue

### Desarrollo
```bash
python app.py
# Servidor: http://localhost:5000
# Debug: True
```

### Producción
```bash
# Opción 1: Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Opción 2: uWSGI
pip install uwsgi
uwsgi --http :8000 --wsgi-file app.py --callable app

# Opción 3: Waitress (Windows)
pip install waitress
waitress-serve --port=8000 app:app
```

### Proxy Inverso (Nginx)
```nginx
server {
    listen 80;
    server_name taller.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 Rendimiento

### Optimizaciones Implementadas
- **CSS inline** en base.html (reduce requests HTTP)
- **Consultas SQL optimizadas** con índices
- **Sesiones ligeras** (solo datos esenciales)
- **Caché de navegador** para assets estáticos
- **Lazy loading** de gráficas (Chart.js)

### Métricas Esperadas
- **Tiempo de carga inicial:** < 1s
- **Tiempo de respuesta API:** < 100ms
- **Tamaño de página:** ~50KB (HTML+CSS)
- **Requests HTTP:** 3-5 por página

---

## 🔄 Versionamiento

### Control de Versiones
- **Git** - Sistema de control de versiones
- **.gitignore** - Excluye archivos sensibles
- **.gitattributes** - Normalización de líneas

### Estructura de Commits
```
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Actualización de documentación
style: Cambios de formato
refactor: Refactorización de código
test: Pruebas
chore: Tareas de mantenimiento
```

---

## 🧪 Testing (Futuro)

### Herramientas Sugeridas
- **pytest** - Testing de Python
- **pytest-flask** - Testing de rutas Flask
- **coverage** - Cobertura de código
- **selenium** - Testing E2E

### Áreas a Testear
- Autenticación y autorización
- CRUD de órdenes
- Generación de folios
- Cálculos financieros
- API REST

---

## 📈 Escalabilidad

### Limitaciones Actuales
- SQLite (no recomendado para >100 usuarios concurrentes)
- Sin caché de aplicación
- Sin CDN para assets

### Mejoras Futuras
- **PostgreSQL/MySQL** - Base de datos más robusta
- **Redis** - Caché de sesiones y datos
- **Celery** - Tareas asíncronas
- **Docker** - Contenedorización
- **Load Balancer** - Múltiples instancias

---

## 🛠 Herramientas de Desarrollo

### Recomendadas
- **VS Code** - Editor de código
- **DB Browser for SQLite** - Explorador de BD
- **Postman** - Testing de API
- **Chrome DevTools** - Debug frontend

### Extensiones VS Code
- Python
- Pylance
- Jinja
- SQLite Viewer

---

## 📚 Referencias

### Documentación Oficial
- [Flask](https://flask.palletsprojects.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [SQLite](https://www.sqlite.org/docs.html)
- [Chart.js](https://www.chartjs.org/docs/)
- [Werkzeug](https://werkzeug.palletsprojects.com/)

### Tutoriales
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Chart.js Getting Started](https://www.chartjs.org/docs/latest/getting-started/)

---

**Versión:** 1.0  
**Última actualización:** 2026-03-12  
**Mantenedor:** Sistema Taller Felinormar
