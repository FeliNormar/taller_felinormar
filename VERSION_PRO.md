# 🔐 Gestión de Versión PRO

Este documento explica cómo mantener dos versiones del sistema: Básica (GitHub) y PRO (Comercial).

## 📊 Diferencias entre Versiones

### Versión BÁSICA (GitHub - Código Abierto)
```
✅ Usuario admin único
✅ Gestión de órdenes
✅ Dashboard con estadísticas
✅ Catálogo de reparaciones
✅ Gestión de usuarios
✅ Mensajes de WhatsApp
```

### Versión PRO (Ejecutable - Comercial)
```
✅ Todo lo de la versión básica
✨ Rol de ventas (permisos limitados)
✨ Configuración del taller personalizable
✨ Nombre del taller editable
✨ Nombre del propietario editable
✨ Ubicación personalizable
✨ Mensajes WhatsApp con datos del taller
```

---

## 📁 Archivos Exclusivos PRO

Estos archivos NO se suben a Git:

### Nuevos Archivos PRO:
```
app/routes/configuracion.py       # Blueprint de configuración
templates/configuracion.html      # Formulario de configuración
```

### Archivos Modificados para PRO:
```
scripts/setup_db.py               # Tabla configuracion + usuario ventas
app/utils/helpers.py              # WhatsApp con configuración dinámica
app/__init__.py                   # Registro blueprint configuración
templates/base.html               # Menú según rol + enlace configuración
```

---

## 🛠️ Flujo de Trabajo

### Para Cambios en Versión BÁSICA:

1. **Edita archivos básicos**
2. **Prueba localmente**
3. **Commit y push a GitHub:**
   ```bash
   git add .
   git commit -m "feat: descripción del cambio"
   git push origin main
   ```

### Para Cambios en Versión PRO:

1. **Edita archivos PRO** (los del .gitignore)
2. **Prueba localmente**
3. **Regenera el .exe:**
   ```bash
   pyinstaller --clean --noconfirm TallerFelinormar.spec
   ```
4. **NO hagas commit** de archivos PRO
5. **Distribuye el .exe** actualizado

---

## 🔄 Sincronización de Versiones

### Cuando actualizas código básico:

```bash
# 1. Actualiza código básico
git pull origin main

# 2. Aplica cambios PRO manualmente
# (edita archivos PRO según sea necesario)

# 3. Regenera .exe
pyinstaller --clean --noconfirm TallerFelinormar.spec

# 4. Prueba el .exe
dist/TallerFelinormar.exe
```

---

## 🚫 Protección contra Subidas Accidentales

El `.gitignore` está configurado para ignorar:

```gitignore
# Funciones PRO
app/routes/configuracion.py
templates/configuracion.html
```

### Verificar antes de commit:

```bash
# Ver qué archivos se van a subir
git status

# Si ves archivos PRO, NO hagas commit
# Verifica que estén en .gitignore
```

---

## 📦 Distribución

### Versión BÁSICA:
- **Dónde:** GitHub público
- **Cómo:** `git push origin main`
- **Quién:** Cualquiera puede clonar
- **Uso:** Demo, evaluación, aprendizaje

### Versión PRO:
- **Dónde:** Tu PC local / Releases privados
- **Cómo:** Compartir `TallerFelinormar.exe`
- **Quién:** Solo clientes que paguen
- **Uso:** Comercial con licencia

---

## 🎯 Estrategia de Venta

### Modelo Freemium:

1. **Versión Básica (Gratis):**
   - Disponible en GitHub
   - Funcionalidad completa básica
   - Sirve como demo/marketing
   - Usuarios pueden probar el sistema

2. **Versión PRO (Pago):**
   - Funciones exclusivas
   - Personalización completa
   - Soporte prioritario
   - Actualizaciones incluidas

### Precios Sugeridos:

```
Trial (15 días):        Gratis
Licencia Básica:        Gratis (GitHub)
Licencia PRO:           $50-100 USD (pago único)
Licencia Empresarial:   $200-500 USD (anual)
```

---

## 🔐 Seguridad

### Proteger Código PRO:

1. **Nunca subir a Git público**
2. **Ofuscar código en .exe** (PyInstaller lo hace)
3. **Agregar sistema de licencias** (futuro)
4. **Backups locales** de archivos PRO

### Backup de Archivos PRO:

```bash
# Crear backup
mkdir backups_pro
cp app/routes/configuracion.py backups_pro/
cp templates/configuracion.html backups_pro/
cp scripts/setup_db.py backups_pro/setup_db_pro.py
# etc...
```

---

## 📝 Checklist antes de Distribuir

### Versión BÁSICA (GitHub):
- [ ] Código funciona correctamente
- [ ] Sin archivos PRO en commit
- [ ] Documentación actualizada
- [ ] README claro
- [ ] Tests pasando (si aplica)

### Versión PRO (.exe):
- [ ] Todas las funciones PRO funcionan
- [ ] Configuración del taller funciona
- [ ] Rol de ventas funciona
- [ ] Base de datos se crea correctamente
- [ ] .exe probado en PC limpia
- [ ] Instrucciones actualizadas

---

## 🆘 Solución de Problemas

### "Subí archivos PRO por error"

```bash
# 1. Revertir último commit
git reset --hard HEAD~1

# 2. Forzar push
git push origin main --force

# 3. Verificar .gitignore
cat .gitignore | grep configuracion
```

### "Perdí archivos PRO"

```bash
# 1. Buscar en backups
ls backups_pro/

# 2. O regenerar desde .exe
# (el .exe tiene el código compilado)
```

### "Conflicto entre versiones"

```bash
# 1. Mantén archivos PRO separados
# 2. Usa nombres diferentes si es necesario:
#    - helpers.py (básico)
#    - helpers_pro.py (PRO)
```

---

## 📊 Estadísticas de Uso

### Tracking (Opcional):

Puedes agregar analytics para saber:
- Cuántas instalaciones básicas
- Cuántas licencias PRO vendidas
- Funciones más usadas

---

## 🎯 Roadmap

### Futuras Funciones PRO:

- [ ] Sistema de licencias automático
- [ ] Reportes avanzados en PDF
- [ ] Integración con facturación
- [ ] Multi-sucursal
- [ ] API REST
- [ ] App móvil

---

**Desarrollado por:** Felipe Norberto Marcelino  
**Versión Básica:** GitHub (Gratis)  
**Versión PRO:** Comercial (Licencia)  
**Fecha:** Marzo 2026
