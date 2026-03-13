@echo off
REM Script para generar ejecutable .exe de Taller Felinormar
REM Desarrollado por: Felipe Norberto Marcelino

title Generador de Ejecutable - Taller Felinormar
color 0B

echo ========================================
echo   TALLER FELINORMAR
echo   Generador de Ejecutable .exe
echo ========================================
echo.
echo Desarrollado por: Felipe Norberto Marcelino
echo.
echo ========================================
echo.

REM Verificar si PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [INFO] PyInstaller no esta instalado
    echo [INFO] Instalando PyInstaller...
    echo.
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Error al instalar PyInstaller
        pause
        exit /b 1
    )
    echo [OK] PyInstaller instalado
    echo.
)

echo [INFO] Generando ejecutable...
echo [INFO] Esto puede tomar varios minutos...
echo.

REM Generar ejecutable usando el spec file
pyinstaller --clean --noconfirm TallerFelinormar.spec

if errorlevel 1 (
    echo.
    echo [ERROR] Error al generar el ejecutable
    pause
    exit /b 1
)

echo.
echo ========================================
echo   EJECUTABLE GENERADO EXITOSAMENTE
echo ========================================
echo.
echo Ubicacion: dist\TallerFelinormar.exe
echo.
echo IMPORTANTE:
echo - El ejecutable incluye todo lo necesario
echo - NO requiere Python instalado para ejecutarse
echo - La primera ejecucion puede ser lenta
echo - Windows Defender puede marcarlo como desconocido
echo.
echo ========================================
echo.

REM Abrir carpeta dist
if exist "dist\TallerFelinormar.exe" (
    echo [INFO] Abriendo carpeta dist...
    explorer dist
)

pause
