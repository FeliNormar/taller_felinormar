# Script para generar el instalador de Taller Felinormar
# Desarrollado por: Felipe Norberto Marcelino
# Copyright (c) 2026 Felipe Norberto Marcelino

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TALLER FELINORMAR - BUILD INSTALLER" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si Inno Setup está instalado
$innoSetupPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
$innoSetupPath2 = "C:\Program Files\Inno Setup 6\ISCC.exe"

if (Test-Path $innoSetupPath) {
    $iscc = $innoSetupPath
} elseif (Test-Path $innoSetupPath2) {
    $iscc = $innoSetupPath2
} else {
    Write-Host "[ERROR] Inno Setup no está instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Descarga Inno Setup desde:" -ForegroundColor Yellow
    Write-Host "https://jrsoftware.org/isdl.php" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "[OK] Inno Setup encontrado: $iscc" -ForegroundColor Green
Write-Host ""

# Cambiar al directorio del script
Set-Location $PSScriptRoot

# Verificar que existe setup.iss
if (-not (Test-Path "setup.iss")) {
    Write-Host "[ERROR] No se encuentra setup.iss" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "[INFO] Compilando instalador..." -ForegroundColor Yellow
Write-Host ""

# Compilar el instalador
& $iscc "setup.iss"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  INSTALADOR GENERADO EXITOSAMENTE" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    $outputFile = "output\TallerFelinormar_v2.0_Setup.exe"
    if (Test-Path $outputFile) {
        $fileSize = (Get-Item $outputFile).Length / 1MB
        Write-Host "Archivo: $outputFile" -ForegroundColor Cyan
        Write-Host "Tamaño: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "El instalador está listo para distribuir!" -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "[ERROR] Error al compilar el instalador" -ForegroundColor Red
    Write-Host "Revisa los mensajes de error arriba" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Presiona Enter para salir"
