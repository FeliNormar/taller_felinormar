# 🔒 Guía de Seguridad - Taller Felinormar

## ✅ Preparación para Git

El proyecto ya está configurado de forma segura para subirlo a Git:

### Archivos Protegidos (en .gitignore)

✅ **Base de datos**
- `*.db` - La base de datos con información de clientes NO se subirá

✅ **Configuración sensible**
- `config.py` - Contiene SECRET_KEY y configuraciones sensibles
- `.env` - Variables de entorno (si las usas)

✅ **Archivos de usuario**
- `static/uploads/*` - Archivos subidos por usuarios
- `venv/` - Entorno virtual de Python

✅ **Archivos temporales**
- `__pycache__/`, `*.pyc` - Archivos compilados de Python
- `*.log` - Archivos de registro

### Archivos Incluidos en Git

✅ **Código fuente**
- `app.py` - Aplicación principal (sin credenciales hardcodeadas)
- `setup_db.py` - Script de inicialización
- `templates/` - Plantillas HTML
- `static/` - Archivos estáticos (CSS, JS, imágenes)

✅ **Configuración de ejemplo**
- `config.example.py` - Plantilla de configuración (sin datos reales)
- `requirements.txt` - Dependencias del proyecto
- `.gitignore` - Reglas de exclusión

✅ **Documentación**
- `README.md` - Documentación principal
- `SEGURIDAD.md` - Este archivo
- Otros archivos .md

## 🔐 Recomendaciones de Seguridad

### Antes de Subir a Git

1. **Verifica que .gitignore esté funcionando:**
   ```bash
   git status
   # NO deberías ver archivos .db, config.py, o venv/
   ```

2. **Revisa que no haya credenciales en el código:**
   ```bash
   # Buscar posibles secretos
   grep -r "password.*=" --include="*.py" .
   grep -r "secret" --include="*.py" .
   ```

3. **Genera una nueva SECRET_KEY para producción:**
   ```python
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### Para Producción

⚠️ **IMPORTANTE: Antes de desplegar en producción:**

1. **Cambia la SECRET_KEY en config.py:**
   ```python
   SECRET_KEY = "tu_clave_super_secreta_aleatoria_aqui"
   ```

2. **Cambia la contraseña del usuario admin:**
   - Inicia sesión como admin
   - Ve a Usuarios → Nuevo Usuario
   - Crea un nuevo admin con contraseña segura
   - Elimina el usuario admin original

3. **Desactiva el modo DEBUG:**
   ```python
   # En config.py
   DEBUG = False
   ```

4. **Usa HTTPS:**
   - Configura un certificado SSL
   - Usa Nginx o Apache como proxy inverso

5. **Configura permisos de archivos:**
   ```bash
   chmod 600 config.py
   chmod 600 taller_felinormar.db
   ```

6. **Haz respaldos regulares:**
   ```bash
   # Respaldar la base de datos
   cp taller_felinormar.db backup_$(date +%Y%m%d).db
   ```

## 📋 Checklist Pre-Git

Antes de hacer tu primer commit:

- [ ] Verificar que `.gitignore` existe
- [ ] Confirmar que `config.py` está en `.gitignore`
- [ ] Confirmar que `*.db` está en `.gitignore`
- [ ] Revisar que no hay contraseñas hardcodeadas en el código
- [ ] Verificar que `config.example.py` existe (sin datos reales)
- [ ] Documentación actualizada (README.md)

## 🚀 Comandos Git Seguros

```bash
# 1. Inicializar repositorio
git init

# 2. Verificar qué archivos se incluirán
git status

# 3. Agregar archivos (el .gitignore protegerá los sensibles)
git add .

# 4. Verificar nuevamente antes de commit
git status

# 5. Hacer commit
git commit -m "Initial commit: Sistema de gestión Taller Felinormar"

# 6. Conectar con GitHub/GitLab
git remote add origin https://github.com/tu-usuario/taller-felinormar.git

# 7. Subir a Git
git push -u origin main
```

## ⚠️ Qué NO Subir NUNCA a Git

❌ Base de datos con información real de clientes
❌ Archivos de configuración con credenciales reales
❌ Claves API o tokens de acceso
❌ Contraseñas en texto plano
❌ Información personal identificable (PII)
❌ Certificados SSL privados
❌ Archivos de respaldo (.bak, .backup)

## ✅ Qué SÍ Puedes Subir

✓ Código fuente (sin credenciales)
✓ Templates y archivos estáticos
✓ Archivos de configuración de ejemplo
✓ Documentación
✓ Scripts de inicialización (sin datos sensibles)
✓ Dependencias (requirements.txt)
✓ Tests y scripts de desarrollo

## 🔍 Verificación Final

Después de subir a Git, clona el repositorio en otra carpeta y verifica:

```bash
# Clonar en otra ubicación
git clone https://github.com/tu-usuario/taller-felinormar.git test-clone
cd test-clone

# Verificar que NO existan archivos sensibles
ls -la *.db        # No debería existir
ls -la config.py   # No debería existir

# Verificar que SÍ existan archivos necesarios
ls -la config.example.py  # Debe existir
ls -la app.py             # Debe existir
ls -la .gitignore         # Debe existir
```

---

## 📞 Soporte

Si tienes dudas sobre seguridad:
1. Revisa este documento
2. Consulta la documentación de Flask sobre seguridad
3. Nunca compartas credenciales reales en issues públicos

**Recuerda:** Es mejor ser precavido. Si tienes dudas sobre si un archivo es sensible, NO lo subas a Git.
