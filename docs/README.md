# 📚 Documentación - Taller Felinormar

Documentación esencial del sistema de gestión de reparaciones.

---

## 📑 Documentos Disponibles

### 🚀 Despliegue y Producción
**[DEPLOYMENT.md](DEPLOYMENT.md)** - Guía completa de despliegue  
Cómo desplegar la aplicación en Render, Railway, VPS o Heroku.  
Incluye configuración de Gunicorn, Nginx, SSL y backups.

### 📋 Funcionalidad del Sistema
**[CASOS_DE_USO.md](CASOS_DE_USO.md)** - 12 casos de uso detallados  
Documentación funcional completa con actores, flujos y diagramas.

### 🛠 Stack Tecnológico
**[TECNOLOGIAS.md](TECNOLOGIAS.md)** - Arquitectura y tecnologías  
Descripción detallada del stack, patrones de diseño y decisiones técnicas.

### 🔒 Seguridad
**[SEGURIDAD.md](SEGURIDAD.md)** - Guía de seguridad  
Mejores prácticas, configuración segura y checklist de producción.

### ⚡ Inicio Rápido
**[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Quick start guide  
Guía rápida para iniciar el proyecto en desarrollo.

---

## 🎯 Guías por Objetivo

### Para Desarrolladores Nuevos
1. Lee el **[README principal](../README.md)** para entender el proyecto
2. Sigue **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** para configurar tu entorno
3. Revisa **[TECNOLOGIAS.md](TECNOLOGIAS.md)** para entender la arquitectura
4. Consulta **[CASOS_DE_USO.md](CASOS_DE_USO.md)** para la funcionalidad

### Para Desplegar a Producción
1. Lee **[DEPLOYMENT.md](DEPLOYMENT.md)** completo
2. Revisa **[SEGURIDAD.md](SEGURIDAD.md)** para configuración segura
3. Sigue los pasos específicos de tu plataforma (Render/Railway/VPS)
4. Configura backups y monitoreo

### Para Entender el Sistema
1. **[CASOS_DE_USO.md](CASOS_DE_USO.md)** - Qué hace el sistema
2. **[TECNOLOGIAS.md](TECNOLOGIAS.md)** - Cómo está construido
3. Código fuente en `app/` - Implementación

---

## 📖 Resumen de Documentos

### DEPLOYMENT.md
**Contenido:**
- Estructura del proyecto production-ready
- Configuración local para desarrollo
- Despliegue en Render (paso a paso)
- Despliegue en Railway (paso a paso)
- Despliegue en VPS con Nginx y Supervisor
- Configuración de SSL con Let's Encrypt
- Checklist de seguridad
- Monitoreo y logs
- Backups automáticos
- Solución de problemas comunes

**Cuándo usar:** Antes de desplegar a producción

### CASOS_DE_USO.md
**Contenido:**
- 3 actores del sistema (Admin, Técnico, Cliente)
- 12 casos de uso detallados con flujos
- 4 flujos de trabajo completos
- Diagramas de secuencia
- Reglas de negocio
- Métricas y KPIs
- Glosario de términos

**Cuándo usar:** Para entender la funcionalidad del sistema

### TECNOLOGIAS.md
**Contenido:**
- Diagrama de arquitectura
- Stack completo (Backend + Frontend)
- Patrones de diseño (Factory, MVC, Blueprints)
- Configuración por entorno
- Seguridad implementada
- Integraciones (WhatsApp, QR)
- Guía de despliegue técnico
- Escalabilidad y optimizaciones

**Cuándo usar:** Para entender decisiones técnicas y arquitectura

### SEGURIDAD.md
**Contenido:**
- Configuración segura por entorno
- Variables de entorno
- Protección de datos sensibles
- Checklist de seguridad
- Mejores prácticas
- Configuración de HTTPS
- Gestión de secretos
- Auditoría y logs

**Cuándo usar:** Antes de desplegar y para auditorías

### INICIO_RAPIDO.md
**Contenido:**
- Instalación rápida (5 pasos)
- Configuración de entorno de desarrollo
- Primer inicio de la aplicación
- Credenciales por defecto
- Comandos útiles
- Solución de problemas comunes

**Cuándo usar:** Primera vez que trabajas con el proyecto

---

## 🔍 Búsqueda Rápida

### ¿Cómo inicio el proyecto?
→ [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

### ¿Cómo despliego a producción?
→ [DEPLOYMENT.md](DEPLOYMENT.md)

### ¿Qué tecnologías usa?
→ [TECNOLOGIAS.md](TECNOLOGIAS.md)

### ¿Cómo funciona el sistema?
→ [CASOS_DE_USO.md](CASOS_DE_USO.md)

### ¿Cómo aseguro la aplicación?
→ [SEGURIDAD.md](SEGURIDAD.md)

### ¿Cómo genero SECRET_KEY?
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### ¿Cómo hago backup de la BD?
```bash
cp instance/taller_felinormar.db backups/backup_$(date +%Y%m%d).db
```

### ¿Cómo cambio la contraseña de admin?
1. Accede como admin
2. Ve a Usuarios → Nuevo Usuario
3. Crea nuevo admin con contraseña segura
4. Elimina el admin original

---

## 📊 Estructura de la Documentación

```
docs/
├── README.md              # Este archivo (índice)
├── DEPLOYMENT.md          # Guía de despliegue (ESENCIAL)
├── CASOS_DE_USO.md        # Funcionalidad del sistema
├── TECNOLOGIAS.md         # Stack tecnológico
├── SEGURIDAD.md           # Guía de seguridad
└── INICIO_RAPIDO.md       # Quick start
```

**Total:** 6 documentos esenciales (sin duplicados)

---

## 🎯 Documentación Eliminada (Duplicados)

Se eliminaron los siguientes documentos por contener información duplicada:

- ❌ CHECKLIST_GIT.md (info en DEPLOYMENT.md)
- ❌ LISTO_PARA_GIT.md (info en DEPLOYMENT.md)
- ❌ README_GIT.md (info en README principal)
- ❌ RESUMEN_SEGURIDAD_GIT.txt (info en SEGURIDAD.md)
- ❌ CORRECCIONES.md (histórico, no necesario)
- ❌ VERIFICACION.md (histórico, no necesario)
- ❌ RESUMEN_FINAL.md (info en README principal)

**Resultado:** Documentación más limpia y sin redundancia.

---

## 📞 Soporte

Si tienes dudas:
1. Revisa el documento específico para tu necesidad
2. Consulta el [README principal](../README.md)
3. Revisa los comentarios en el código fuente

---

## 🔄 Mantenimiento de Documentación

### Al Agregar Funcionalidad
1. Actualizar CASOS_DE_USO.md con nuevos casos
2. Actualizar README principal con la feature
3. Si afecta despliegue, actualizar DEPLOYMENT.md

### Al Cambiar Tecnología
1. Actualizar TECNOLOGIAS.md
2. Actualizar requirements.txt
3. Actualizar README principal

### Al Cambiar Configuración
1. Actualizar DEPLOYMENT.md
2. Actualizar .env.example
3. Actualizar SEGURIDAD.md si aplica

---

**Última actualización:** 2026-03-12  
**Versión:** 2.0 (Production-Ready)  
**Documentos:** 6 esenciales
