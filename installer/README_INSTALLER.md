# Generador de Instalador para Windows

Este directorio contiene los archivos necesarios para crear un instalador profesional de Windows (.exe) para Taller Felinormar.

## 📋 Requisitos

### 1. Inno Setup
Descarga e instala Inno Setup (gratuito):
- **URL:** https://jrsoftware.org/isdl.php
- **Versión recomendada:** 6.2.2 o superior
- **Tamaño:** ~3 MB

### 2. Python 3.11+
El instalador verificará que Python esté instalado en el sistema del usuario.

## 🚀 Cómo Generar el Instalador

### Opción 1: Usando Inno Setup GUI (Recomendado)

1. Abre **Inno Setup Compiler**
2. Ve a `File` → `Open` 
3. Selecciona el archivo `setup.iss`
4. Presiona `F9` o ve a `Build` → `Compile`
5. El instalador se generará en `installer/output/TallerFelinormar_v2.0_Setup.exe`

### Opción 2: Línea de Comandos

```cmd
cd installer
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
```

## 📦 Archivos Incluidos en el Instalador

El instalador empaqueta:
- ✅ Aplicación completa (app/, templates/, static/)
- ✅ Scripts de inicio automatizados
- ✅ Documentación (docs/, README.md)
- ✅ Licencia de evaluación (LICENSE)
- ✅ Archivos de configuración
- ✅ Script de instalación de dependencias

## 🎯 Características del Instalador

### Durante la Instalación:
- ✅ Verifica que Python 3.11+ esté instalado
- ✅ Muestra información de la licencia Trial (15 días)
- ✅ Permite elegir directorio de instalación
- ✅ Crea accesos directos en Menú Inicio y Escritorio
- ✅ Instala dependencias automáticamente
- ✅ Inicializa la base de datos

### Después de la Instalación:
- ✅ Opción de ejecutar inmediatamente
- ✅ Acceso directo para iniciar el sistema
- ✅ Acceso a documentación y licencia
- ✅ Desinstalador incluido

## 📁 Estructura de Archivos

```
installer/
├── setup.iss                    # Script principal de Inno Setup
├── iniciar_felinormar.bat      # Script de inicio del sistema
├── instalar_dependencias.bat   # Script de instalación de deps
├── installer_info.txt          # Información pre-instalación
├── icon.ico                    # Icono del instalador (opcional)
├── README_INSTALLER.md         # Esta documentación
└── output/                     # Carpeta de salida (se crea automáticamente)
    └── TallerFelinormar_v2.0_Setup.exe
```

## 🎨 Personalización

### Cambiar el Icono
1. Crea o descarga un archivo `.ico` (32x32 o 64x64 px)
2. Guárdalo como `installer/icon.ico`
3. El script ya está configurado para usarlo

### Cambiar la Versión
Edita `setup.iss` línea 6:
```iss
#define MyAppVersion "2.0"
```

### Cambiar el Nombre del Instalador
Edita `setup.iss` línea 19:
```iss
OutputBaseFilename=TallerFelinormar_v2.0_Setup
```

## 🔧 Solución de Problemas

### Error: "Python not found"
El instalador verifica Python automáticamente. Si no está instalado:
1. El instalador mostrará un mensaje
2. Ofrecerá abrir la página de descarga de Python
3. Instala Python 3.11+ y vuelve a ejecutar el instalador

### Error: "Cannot create output directory"
Ejecuta Inno Setup como Administrador:
- Click derecho en Inno Setup → "Ejecutar como administrador"

### El instalador no incluye todos los archivos
Verifica que todos los archivos estén en sus ubicaciones correctas:
```
taller_felinormar/
├── app/
├── templates/
├── static/
├── docs/
├── scripts/
├── wsgi.py
├── requirements.txt
└── installer/
    └── setup.iss
```

## 📊 Tamaño del Instalador

- **Tamaño aproximado:** 2-5 MB (comprimido con LZMA)
- **Tamaño instalado:** ~15-20 MB (sin venv)
- **Con dependencias:** ~150-200 MB (con venv completo)

## 🚀 Distribución

Una vez generado el instalador:

1. **Prueba local:**
   ```cmd
   installer\output\TallerFelinormar_v2.0_Setup.exe
   ```

2. **Distribución:**
   - Sube a GitHub Releases
   - Comparte el archivo .exe directamente
   - Hospeda en tu sitio web

3. **Firma digital (Opcional):**
   Para producción profesional, considera firmar el instalador con un certificado de código.

## 📝 Notas Importantes

- ⚠️ El instalador requiere permisos de administrador
- ⚠️ Windows Defender puede marcar el .exe como desconocido (normal para apps sin firma)
- ⚠️ Los usuarios deben tener Python 3.11+ instalado
- ✅ El instalador crea un entorno virtual automáticamente
- ✅ La base de datos se inicializa en el primer inicio

## 🔐 Licencia

El instalador incluye la licencia de evaluación de 15 días.
Ver [LICENSE](../LICENSE) para términos completos.

---

**Desarrollado por:** Felipe Norberto Marcelino  
**Versión:** 2.0  
**Fecha:** Marzo 2026
