@echo off
REM Script de instalacion de dependencias
REM Desarrollado por: Felipe Norberto Marcelino

cd /d "%~dp0"

echo Instalando dependencias de Python...
echo.

REM Crear entorno virtual
if not exist "venv\" (
    python -m venv venv
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Actualizar pip
python -m pip install --upgrade pip

REM Instalar dependencias
pip install -r requirements.txt

REM Inicializar base de datos
if not exist "instance\taller_felinormar.db" (
    python scripts\setup_db.py
)

echo.
echo Instalacion completada exitosamente!
echo.

exit /b 0
