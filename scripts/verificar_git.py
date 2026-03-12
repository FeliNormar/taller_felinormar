#!/usr/bin/env python3
"""
Script de verificación pre-Git
Verifica que el proyecto esté listo para subirse a Git de forma segura
"""
import os
import sys

# Cambiar al directorio raíz del proyecto
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

def check_file_exists(filepath, should_exist=True):
    exists = os.path.exists(filepath)
    if should_exist:
        if exists:
            print(f"  ✓ {filepath} existe")
            return True
        else:
            print(f"  ✗ {filepath} NO existe (debería existir)")
            return False
    else:
        if not exists:
            print(f"  ✓ {filepath} NO existe (correcto)")
            return True
        else:
            print(f"  ⚠ {filepath} existe (se excluirá por .gitignore)")
            return True

def check_gitignore():
    print("\n1. Verificando .gitignore...")
    if not os.path.exists('.gitignore'):
        print("  ✗ .gitignore NO existe")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    required = ['*.db', 'config.py', 'venv/', '__pycache__']
    all_ok = True
    for item in required:
        if item in content:
            print(f"  ✓ '{item}' está en .gitignore")
        else:
            print(f"  ✗ '{item}' NO está en .gitignore")
            all_ok = False
    
    return all_ok

def check_config_files():
    print("\n2. Verificando archivos de configuración...")
    ok1 = check_file_exists('config.example.py', should_exist=True)
    ok2 = check_file_exists('config.py', should_exist=True)
    
    if ok2:
        print("  ℹ config.py existe pero NO se subirá a Git (está en .gitignore)")
    
    return ok1

def check_sensitive_files():
    print("\n3. Verificando que NO existan archivos sensibles sin protección...")
    
    # Buscar contraseñas hardcodeadas en app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'felinormar_2025_super_secreto' in content and 'config.SECRET_KEY' not in content:
        print("  ✗ SECRET_KEY hardcodeada encontrada en app.py")
        return False
    else:
        print("  ✓ No se encontró SECRET_KEY hardcodeada en app.py")
    
    return True

def check_documentation():
    print("\n4. Verificando documentación...")
    docs = [
        ('README.md', True),
        ('docs/SEGURIDAD.md', True),
        ('requirements.txt', True)
    ]
    all_ok = True
    for doc, should_exist in docs:
        if not check_file_exists(doc, should_exist=should_exist):
            all_ok = False
    return all_ok

def check_database():
    print("\n5. Verificando base de datos...")
    if os.path.exists('taller_felinormar.db'):
        print("  ⚠ Base de datos existe (NO se subirá a Git por .gitignore)")
        print("    Esto es correcto - la BD no debe subirse a Git")
        return True
    else:
        print("  ℹ Base de datos no existe (se creará con setup_db.py)")
        return True

def main():
    print("=" * 60)
    print("  VERIFICACIÓN PRE-GIT - Taller Felinormar")
    print("=" * 60)
    
    checks = [
        check_gitignore(),
        check_config_files(),
        check_sensitive_files(),
        check_documentation(),
        check_database()
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ VERIFICACIÓN EXITOSA")
        print("   El proyecto está listo para subirse a Git de forma segura")
        print("\nPróximos pasos:")
        print("  1. git init")
        print("  2. git add .")
        print("  3. git commit -m 'Initial commit'")
        print("  4. git remote add origin <tu-repo-url>")
        print("  5. git push -u origin main")
    else:
        print("❌ VERIFICACIÓN FALLIDA")
        print("   Corrige los errores antes de subir a Git")
        sys.exit(1)
    print("=" * 60)

if __name__ == '__main__':
    main()
