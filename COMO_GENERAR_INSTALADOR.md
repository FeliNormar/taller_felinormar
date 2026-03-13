# 🚀 Cómo Generar el Instalador de Windows

Guía rápida para crear el instalador `.exe` de Taller Felinormar.

## 📋 Requisitos Previos

### 1. Descargar Inno Setup (GRATIS)
- **URL:** https://jrsoftware.org/isdl.php
- **Versión:** 6.2.2 o superior
- **Tamaño:** ~3 MB
- **Instalación:** Siguiente → Siguiente → Instalar

## 🎯 Método 1: Automático (Recomendado)

### Paso 1: Abrir PowerShell
```powershell
cd taller_felinormar\installer
```

### Paso 2: Ejecutar el script
```powershell
.\build_installer.ps1
```

### Paso 3: ¡Listo!
El instalador se generará en:
```
installer\output\TallerFelinormar_v2.0_Setup.exe
```

## 🎯 Método 2: Manual con Inno Setup

### Paso 1: Abrir Inno Setup Compiler
- Busca "Inno Setup Compiler" en el menú de Windows
- Ábrelo

### Paso 2: Abrir el script
- Ve a `File` → `Open`
- Navega a `taller_felinormar\installer\`
- Selecciona `setup.iss`

### Paso 3: Compilar
- Presiona `F9` o
- Ve a `Build` → `Compile`

### Paso 4: ¡Listo!
El instalador se generará en:
```
installer\output\TallerFelinormar_v2.0_Setup.exe
```

## 📦 Qué Incluye el Instalador

✅ Aplicación completa  
✅ Scripts de inicio automatizados  
✅ Instalación de dependencias automática  
✅ Inicialización de base de datos  
✅ Accesos directos en Menú Inicio  
✅ Opción de icono en Escritorio  
✅ Desinstalador incluido  
✅ Verificación de Python 3.11+  

## 🎨 Personalización (Opcional)

### Cambiar el Icono
1. Crea o descarga un archivo `.ico` (32x32 o 64x64 px)
2. Guárdalo como `installer\icon.ico`
3. Vuelve a compilar

### Cambiar la Versión
Edita `installer\setup.iss` línea 6:
```iss
#define MyAppVersion "2.1"
```

## 🚀 Distribución

Una vez generado el instalador:

### Opción 1: GitHub Releases
1. Ve a tu repositorio en GitHub
2. Click en "Releases" → "Create a new release"
3. Sube el archivo `.exe`
4. Publica el release

### Opción 2: Compartir Directamente
- Envía el archivo `.exe` por email
- Súbelo a Google Drive / Dropbox
- Compártelo en tu sitio web

## ⚠️ Notas Importantes

- El instalador requiere permisos de administrador
- Windows Defender puede marcar el .exe como "desconocido" (es normal para apps sin firma digital)
- Los usuarios necesitan Python 3.11+ instalado
- El instalador lo verificará automáticamente

## 🔧 Solución de Problemas

### "Inno Setup no encontrado"
- Verifica que Inno Setup esté instalado en:
  - `C:\Program Files (x86)\Inno Setup 6\`
  - `C:\Program Files\Inno Setup 6\`

### "Error al compilar"
- Ejecuta Inno Setup como Administrador
- Verifica que todos los archivos estén en su lugar

### "Python not found" (al instalar)
- El usuario debe instalar Python 3.11+ desde:
  - https://www.python.org/downloads/

## 📊 Tamaños

- **Instalador comprimido:** ~2-5 MB
- **Instalado (sin dependencias):** ~15-20 MB
- **Con dependencias completas:** ~150-200 MB

## 🎯 Próximos Pasos

Después de generar el instalador:

1. **Pruébalo localmente:**
   ```cmd
   installer\output\TallerFelinormar_v2.0_Setup.exe
   ```

2. **Crea un Release en GitHub:**
   - Tag: `v2.0`
   - Título: "Taller Felinormar v2.0"
   - Descripción: Características principales
   - Adjunta el `.exe`

3. **Comparte con tus usuarios:**
   - Envía el link del Release
   - O comparte el archivo directamente

---

**Desarrollado por:** Felipe Norberto Marcelino  
**Licencia:** Trial 15 días + Comercial  
**Versión:** 2.0
