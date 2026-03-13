# 🚀 Cómo Generar el Ejecutable .exe

Guía para convertir Taller Felinormar en un archivo `.exe` ejecutable standalone.

## 📋 ¿Qué es esto?

Convierte tu aplicación Python en un archivo `.exe` que:
- ✅ Se ejecuta sin necesidad de tener Python instalado
- ✅ Incluye todas las dependencias
- ✅ Es un solo archivo portable
- ✅ Abre el navegador automáticamente
- ✅ Fácil de distribuir

## 🎯 Método Rápido (Recomendado)

### Paso 1: Instalar PyInstaller
```cmd
pip install pyinstaller
```

### Paso 2: Generar el .exe
```cmd
generar_exe.bat
```

### Paso 3: ¡Listo!
El ejecutable estará en:
```
dist\TallerFelinormar.exe
```

## 🎯 Método Manual

### Opción A: Usando el archivo .spec
```cmd
pyinstaller --clean --noconfirm TallerFelinormar.spec
```

### Opción B: Comando directo
```cmd
pyinstaller --onefile --name=TallerFelinormar ^
  --add-data="templates;templates" ^
  --add-data="static;static" ^
  --add-data="app;app" ^
  --hidden-import=flask ^
  --hidden-import=werkzeug ^
  wsgi.py
```

## 📦 Características del .exe

### Ventajas:
- ✅ **Portable:** Un solo archivo, llévalo a cualquier PC
- ✅ **Sin instalación:** Solo doble click y funciona
- ✅ **Sin Python:** No requiere Python instalado
- ✅ **Auto-navegador:** Abre el navegador automáticamente
- ✅ **Base de datos incluida:** SQLite embebido

### Limitaciones:
- ⚠️ Tamaño grande (~50-100 MB) porque incluye Python completo
- ⚠️ Primera ejecución lenta (descomprime archivos)
- ⚠️ Windows Defender puede marcarlo como "desconocido"

## 🔧 Solución de Problemas

### Error: "PyInstaller not found"
```cmd
pip install pyinstaller
```

### Error: "Failed to execute script"
- Verifica que todos los archivos estén en su lugar
- Ejecuta desde la carpeta raíz del proyecto

### Windows Defender bloquea el .exe
Es normal para ejecutables sin firma digital:
1. Click en "Más información"
2. Click en "Ejecutar de todas formas"

### El .exe es muy grande
Es normal, incluye:
- Python completo (~40 MB)
- Flask y dependencias (~20 MB)
- Tu aplicación (~10 MB)

## 📊 Tamaños Aproximados

- **Ejecutable:** ~50-100 MB
- **Descomprimido en memoria:** ~150-200 MB
- **Base de datos:** Crece según uso

## 🎨 Personalización

### Agregar un Icono
1. Crea o descarga un archivo `.ico`
2. Edita `TallerFelinormar.spec` línea 58:
   ```python
   icon='mi_icono.ico'
   ```
3. Regenera el .exe

### Ocultar la Consola
Edita `TallerFelinormar.spec` línea 56:
```python
console=False  # Cambia True a False
```

### Cambiar el Nombre
Edita `TallerFelinormar.spec` línea 48:
```python
name='MiNombre'
```

## 🚀 Distribución

### Opción 1: Compartir el .exe directamente
- Envía `dist\TallerFelinormar.exe` por email
- Súbelo a Google Drive / Dropbox
- Compártelo en tu sitio web

### Opción 2: GitHub Releases
1. Ve a tu repositorio en GitHub
2. Click en "Releases" → "Create a new release"
3. Sube el archivo `.exe`
4. Publica el release

### Opción 3: Crear un ZIP
```cmd
cd dist
tar -a -c -f TallerFelinormar_v2.0.zip TallerFelinormar.exe
```

## 📝 Instrucciones para Usuarios

Cuando compartas el .exe, incluye estas instrucciones:

```
TALLER FELINORMAR v2.0
======================

INSTALACIÓN:
1. Descarga TallerFelinormar.exe
2. Guárdalo en una carpeta (ej: C:\TallerFelinormar\)
3. Doble click en TallerFelinormar.exe

PRIMER USO:
- La primera ejecución puede tardar 10-30 segundos
- Se abrirá automáticamente tu navegador
- Si no se abre, ve a: http://127.0.0.1:5000

CREDENCIALES:
- Usuario: admin
- Contraseña: admin123

IMPORTANTE:
- NO muevas el .exe mientras esté ejecutándose
- Para cerrar: Presiona Ctrl+C en la ventana negra
- La base de datos se crea en la misma carpeta

LICENCIA:
- Trial gratuito de 15 días
- Contacto: Felipe Norberto Marcelino
```

## ⚠️ Notas Importantes

### Seguridad:
- El .exe NO está firmado digitalmente
- Windows Defender lo marcará como "desconocido"
- Es seguro, pero los usuarios deben confiar en ti

### Rendimiento:
- Primera ejecución: 10-30 segundos (descomprime)
- Ejecuciones siguientes: 5-10 segundos
- Una vez iniciado: rendimiento normal

### Base de Datos:
- Se crea en la misma carpeta que el .exe
- Archivo: `taller_felinormar.db`
- Haz backups regularmente

## 🔐 Firma Digital (Opcional)

Para producción profesional, considera firmar el .exe:

1. Compra un certificado de firma de código (~$100-300/año)
2. Usa `signtool.exe` de Windows SDK
3. Esto elimina las advertencias de Windows Defender

## 📚 Recursos Adicionales

- **PyInstaller Docs:** https://pyinstaller.org/
- **Firma de código:** https://docs.microsoft.com/en-us/windows/win32/seccrypto/signtool

---

**Desarrollado por:** Felipe Norberto Marcelino  
**Licencia:** Trial 15 días + Comercial  
**Versión:** 2.0
