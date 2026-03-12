#!/bin/bash
echo "========================================"
echo "  Taller Felinormar - Sistema de Gestión"
echo "========================================"
echo ""
echo "Iniciando servidor Flask..."
echo "Abre tu navegador en: http://localhost:5000"
echo "Usuario: admin"
echo "Contraseña: admin123"
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
cd "$(dirname "$0")/.."
python3 app.py
