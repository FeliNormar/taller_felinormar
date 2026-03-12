# 🔧 Scripts del Proyecto

Esta carpeta contiene scripts de utilidad para el sistema Taller Felinormar.

## 📜 Scripts Disponibles

### 🚀 Scripts de Inicio

#### `iniciar.bat` (Windows)
Script para iniciar la aplicación en Windows.

**Uso:**
```bash
# Opción 1: Doble clic en el archivo
iniciar.bat

# Opción 2: Desde la terminal
cd scripts
iniciar.bat
```

**Qué hace:**
1. Muestra información del sistema
2. Cambia al directorio raíz del proyecto
3. Inicia el servidor Flask
4. Muestra credenciales por defecto

#### `iniciar.sh` (Linux/Mac)
Script para iniciar la aplicación en Linux/Mac.

**Uso:**
```bash
# Dar permisos de ejecución (solo la primera vez)
chmod +x scripts/iniciar.sh

# Ejecutar
./scripts/iniciar.sh
```

**Qué hace:**
1. Muestra información del sistema
2. Cambia al directorio raíz del proyecto
3. Inicia el servidor Flask con Python 3
4. Muestra credenciales por defecto

---

### 🗄️ Scripts de Base de Datos

#### `setup_db.py`
Script para inicializar o migrar la base de datos.

**Uso:**
```bash
# Desde la carpeta scripts
cd scripts
python setup_db.py

# O desde la raíz del proyecto
python scripts/setup_db.py
```

**Qué hace:**
1. Crea las tablas si no existen:
   - `usuarios` - Usuarios del sistema
   - `clientes` - Información de clientes
   - `ordenes` - Órdenes de servicio
   - `reparaciones` - Catálogo de servicios
2. Agrega columnas faltantes (migración)
3. Crea usuario admin por defecto (admin/admin123)
4. Agrega reparaciones de ejemplo si la tabla está vacía

**Cuándo usarlo:**
- Primera instalación del sistema
- Después de clonar desde Git
- Para resetear la base de datos (elimina el .db primero)
- Para agregar nuevas columnas (migración)

**Salida esperada:**
```
Inicializando base de datos 'taller_felinormar.db'...

✓ Base de datos lista: /ruta/completa/taller_felinormar.db
  Usuario por defecto → admin / admin123
  ¡Cambia la contraseña después del primer inicio de sesión!
```

---

### ✅ Scripts de Verificación

#### `verificar_git.py`
Script para verificar que el proyecto esté listo para subirse a Git de forma segura.

**Uso:**
```bash
# Desde la carpeta scripts
cd scripts
python verificar_git.py

# O desde la raíz del proyecto
python scripts/verificar_git.py
```

**Qué verifica:**
1. **`.gitignore` existe y contiene:**
   - `*.db` (base de datos)
   - `config.py` (configuración sensible)
   - `venv/` (entorno virtual)
   - `__pycache__/` (archivos compilados)

2. **Archivos de configuración:**
   - `config.example.py` existe (plantilla)
   - `config.py` existe (pero NO se sube a Git)

3. **Sin credenciales hardcodeadas:**
   - No hay SECRET_KEY en app.py
   - Configuración externa correcta

4. **Documentación completa:**
   - README.md existe
   - SEGURIDAD.md existe
   - requirements.txt existe

5. **Base de datos:**
   - Verifica que existe pero NO se subirá a Git

**Salida esperada (éxito):**
```
============================================================
  VERIFICACIÓN PRE-GIT - Taller Felinormar
============================================================

1. Verificando .gitignore...
  ✓ '*.db' está en .gitignore
  ✓ 'config.py' está en .gitignore
  ✓ 'venv/' está en .gitignore
  ✓ '__pycache__' está en .gitignore

2. Verificando archivos de configuración...
  ✓ config.example.py existe
  ✓ config.py existe
  ℹ config.py existe pero NO se subirá a Git

3. Verificando que NO existan archivos sensibles...
  ✓ No se encontró SECRET_KEY hardcodeada en app.py

4. Verificando documentación...
  ✓ README.md existe
  ✓ SEGURIDAD.md existe
  ✓ requirements.txt existe

5. Verificando base de datos...
  ⚠ Base de datos existe (NO se subirá a Git)

============================================================
✅ VERIFICACIÓN EXITOSA
   El proyecto está listo para subirse a Git de forma segura

Próximos pasos:
  1. git init
  2. git add .
  3. git commit -m 'Initial commit'
  4. git remote add origin <tu-repo-url>
  5. git push -u origin main
============================================================
```

**Cuándo usarlo:**
- Antes de hacer el primer commit
- Antes de hacer push a Git
- Después de modificar archivos de configuración
- Para verificar que no se suban archivos sensibles

---

## 🔄 Flujo de Trabajo Recomendado

### Primera Instalación
```bash
# 1. Clonar o descargar el proyecto
git clone <repo-url>
cd taller_felinormar

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar configuración de ejemplo
cp config.example.py config.py

# 5. Inicializar base de datos
python scripts/setup_db.py

# 6. Iniciar aplicación
./scripts/iniciar.sh      # Linux/Mac
scripts\iniciar.bat       # Windows
```

### Antes de Subir a Git
```bash
# 1. Verificar que todo esté listo
python scripts/verificar_git.py

# 2. Si la verificación pasa, proceder con Git
git init
git add .
git commit -m "Initial commit"
git push
```

### Desarrollo Diario
```bash
# Iniciar la aplicación
./scripts/iniciar.sh      # Linux/Mac
scripts\iniciar.bat       # Windows

# O directamente
python app.py
```

---

## 🛠 Personalización de Scripts

### Modificar Puerto del Servidor
Edita `app.py` en la raíz del proyecto:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Cambia 5000 por el puerto deseado
```

### Agregar Nuevas Migraciones
Edita `scripts/setup_db.py` y agrega en la función `migrate()`:
```python
# Ejemplo: Agregar nueva columna
if not column_exists(conn, 'ordenes', 'nueva_columna'):
    c.execute("ALTER TABLE ordenes ADD COLUMN nueva_columna TEXT")
    print("  Migrado: ordenes.nueva_columna")
```

### Crear Nuevos Scripts
Coloca tus scripts personalizados en esta carpeta y documéntalos aquí.

---

## ⚠️ Notas Importantes

### Scripts de Inicio
- Los scripts de inicio (`iniciar.bat` y `iniciar.sh`) están diseñados para ejecutarse desde la carpeta `scripts/`
- Automáticamente cambian al directorio raíz del proyecto antes de ejecutar `app.py`
- Si ejecutas `python app.py` directamente desde la raíz, no necesitas los scripts

### Script de Base de Datos
- `setup_db.py` es **idempotente**: puedes ejecutarlo múltiples veces sin problemas
- No elimina datos existentes, solo agrega lo que falta
- Si quieres resetear completamente la BD, elimina el archivo `.db` primero

### Script de Verificación
- `verificar_git.py` NO modifica archivos, solo verifica
- Es seguro ejecutarlo en cualquier momento
- Si falla, lee los mensajes de error y corrige los problemas

---

## 📚 Documentación Relacionada

- **[../docs/INICIO_RAPIDO.md](../docs/INICIO_RAPIDO.md)** - Guía de inicio rápido
- **[../docs/LISTO_PARA_GIT.md](../docs/LISTO_PARA_GIT.md)** - Preparación para Git
- **[../docs/SEGURIDAD.md](../docs/SEGURIDAD.md)** - Guía de seguridad
- **[../README.md](../README.md)** - Documentación principal

---

**Última actualización:** 2026-03-12  
**Versión:** 1.0
