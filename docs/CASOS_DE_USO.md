# 📋 Casos de Uso - Sistema Taller Felinormar

## Índice
1. [Actores del Sistema](#actores-del-sistema)
2. [Casos de Uso por Actor](#casos-de-uso-por-actor)
3. [Casos de Uso Detallados](#casos-de-uso-detallados)
4. [Flujos de Trabajo](#flujos-de-trabajo)
5. [Diagramas de Secuencia](#diagramas-de-secuencia)

---

## Actores del Sistema

### 👤 Administrador
Usuario con permisos completos sobre el sistema.

**Permisos:**
- ✅ Gestión completa de órdenes de servicio
- ✅ Acceso al dashboard analítico
- ✅ Gestión de usuarios (crear, eliminar)
- ✅ Gestión del catálogo de reparaciones
- ✅ Configuración del sistema

### 🔧 Técnico
Usuario con permisos limitados para operaciones diarias.

**Permisos:**
- ✅ Gestión de órdenes de servicio (crear, editar, ver)
- ✅ Acceso al dashboard analítico
- ❌ NO puede gestionar usuarios
- ❌ NO puede modificar catálogo de reparaciones

### 📱 Cliente
Usuario externo que recibe servicios (no accede al sistema).

**Interacciones:**
- Recibe notificaciones por WhatsApp
- Recibe etiqueta con código QR de su equipo
- Recibe comprobante de garantía

---

## Casos de Uso por Actor

### Administrador

| ID | Caso de Uso | Prioridad |
|----|-------------|-----------|
| CU-01 | Iniciar sesión | Alta |
| CU-02 | Crear nueva orden de servicio | Alta |
| CU-03 | Consultar órdenes de servicio | Alta |
| CU-04 | Editar orden de servicio | Alta |
| CU-05 | Actualizar estatus de orden | Alta |
| CU-06 | Generar código QR de orden | Media |
| CU-07 | Enviar notificación WhatsApp | Media |
| CU-08 | Ver dashboard analítico | Media |
| CU-09 | Crear usuario | Alta |
| CU-10 | Eliminar usuario | Media |
| CU-11 | Gestionar catálogo de reparaciones | Media |
| CU-12 | Cerrar sesión | Alta |

### Técnico

| ID | Caso de Uso | Prioridad |
|----|-------------|-----------|
| CU-01 | Iniciar sesión | Alta |
| CU-02 | Crear nueva orden de servicio | Alta |
| CU-03 | Consultar órdenes de servicio | Alta |
| CU-04 | Editar orden de servicio | Alta |
| CU-05 | Actualizar estatus de orden | Alta |
| CU-06 | Generar código QR de orden | Media |
| CU-07 | Enviar notificación WhatsApp | Media |
| CU-08 | Ver dashboard analítico | Media |
| CU-12 | Cerrar sesión | Alta |

---

## Casos de Uso Detallados

### CU-01: Iniciar Sesión

**Actor:** Administrador, Técnico

**Descripción:** El usuario accede al sistema mediante credenciales.

**Precondiciones:**
- El usuario debe estar registrado en el sistema
- El usuario debe tener credenciales válidas

**Flujo Principal:**
1. El usuario accede a la URL del sistema
2. El sistema muestra la pantalla de login
3. El usuario ingresa su nombre de usuario
4. El usuario ingresa su contraseña
5. El usuario hace clic en "Iniciar Sesión"
6. El sistema valida las credenciales
7. El sistema crea una sesión para el usuario
8. El sistema redirige al dashboard principal

**Flujo Alternativo 1: Credenciales Incorrectas**
- 6a. Las credenciales son incorrectas
- 6b. El sistema muestra mensaje de error
- 6c. El usuario puede intentar nuevamente

**Postcondiciones:**
- El usuario tiene una sesión activa
- El usuario puede acceder a las funcionalidades según su rol

---

### CU-02: Crear Nueva Orden de Servicio

**Actor:** Administrador, Técnico

**Descripción:** Registrar un nuevo equipo que ingresa al taller.

**Precondiciones:**
- El usuario debe estar autenticado
- El sistema debe tener al menos una reparación en el catálogo

**Flujo Principal:**
1. El usuario hace clic en "Nueva Orden"
2. El sistema muestra el formulario de nueva orden
3. El usuario ingresa datos del cliente:
   - Nombre completo
   - Teléfono de contacto
4. El usuario ingresa datos del equipo:
   - Marca
   - Modelo
   - IMEI (opcional)
   - Contraseña del dispositivo (opcional)
5. El usuario describe el problema reportado
6. El usuario selecciona el tipo de reparación del catálogo
7. El sistema autocompleta el costo según la reparación
8. El usuario puede modificar el costo total
9. El usuario ingresa el anticipo recibido
10. El usuario agrega notas internas (opcional)
11. El usuario hace clic en "Crear Orden"
12. El sistema genera un folio único (FN-XXXX)
13. El sistema registra la fecha de ingreso automáticamente
14. El sistema asigna el técnico que creó la orden
15. El sistema guarda la orden con estatus "Recibido"
16. El sistema redirige al detalle de la orden creada

**Flujo Alternativo 1: Cliente Existente**
- 3a. El sistema detecta que el teléfono ya existe
- 3b. El sistema reutiliza los datos del cliente

**Flujo Alternativo 2: Campos Obligatorios Vacíos**
- 11a. Faltan campos obligatorios
- 11b. El sistema muestra mensaje de error
- 11c. El usuario completa los campos faltantes

**Postcondiciones:**
- Se crea una nueva orden en el sistema
- Se genera un folio único
- El cliente queda registrado (si es nuevo)
- La orden tiene estatus "Recibido"

**Datos de Entrada:**
- Nombre del cliente (requerido)
- Teléfono (requerido)
- Marca del equipo (requerido)
- Modelo del equipo (requerido)
- Problema reportado (requerido)
- IMEI (opcional)
- Contraseña del dispositivo (opcional)
- Tipo de reparación (opcional)
- Costo total (requerido)
- Anticipo (opcional)
- Notas internas (opcional)

**Datos de Salida:**
- Folio generado
- Orden completa registrada

---

### CU-03: Consultar Órdenes de Servicio

**Actor:** Administrador, Técnico

**Descripción:** Visualizar y buscar órdenes de servicio registradas.

**Precondiciones:**
- El usuario debe estar autenticado

**Flujo Principal:**
1. El usuario accede al dashboard principal
2. El sistema muestra todas las órdenes ordenadas por fecha
3. El sistema muestra estadísticas por estatus:
   - Total de órdenes recibidas
   - Total en proceso
   - Total listas
   - Total entregadas
4. El usuario puede ver información resumida de cada orden:
   - Folio
   - Cliente y teléfono
   - Equipo (marca y modelo)
   - Problema
   - Estatus actual
   - Fecha de ingreso
   - Costo total

**Flujo Alternativo 1: Filtrar por Estatus**
- 3a. El usuario hace clic en un filtro de estatus
- 3b. El sistema muestra solo órdenes con ese estatus

**Flujo Alternativo 2: Buscar Orden**
- 3a. El usuario ingresa texto en el buscador
- 3b. El usuario hace clic en "Buscar"
- 3c. El sistema busca coincidencias en:
  - Folio
  - Nombre del cliente
  - Modelo del equipo
- 3d. El sistema muestra resultados filtrados

**Flujo Alternativo 3: Ver Detalle**
- 4a. El usuario hace clic en "Ver" de una orden
- 4b. El sistema redirige al detalle completo (CU-04)

**Postcondiciones:**
- El usuario visualiza las órdenes según filtros aplicados

---

### CU-04: Ver Detalle de Orden

**Actor:** Administrador, Técnico

**Descripción:** Visualizar información completa de una orden específica.

**Precondiciones:**
- El usuario debe estar autenticado
- La orden debe existir en el sistema

**Flujo Principal:**
1. El usuario accede al detalle de una orden
2. El sistema muestra información completa:
   - **Datos del cliente:**
     - Nombre
     - Teléfono
   - **Datos del equipo:**
     - Marca y modelo
     - IMEI
     - Contraseña del dispositivo
   - **Datos de la reparación:**
     - Problema reportado
     - Tipo de reparación
     - Estatus actual
     - Técnico asignado
     - Notas internas
   - **Datos financieros:**
     - Costo total
     - Anticipo
     - Saldo pendiente
   - **Fechas:**
     - Fecha de ingreso
     - Fecha de entrega (si aplica)
3. El sistema genera código QR automáticamente
4. El sistema muestra opciones disponibles según estatus

**Flujo Alternativo 1: Orden Lista**
- 4a. El estatus es "Listo"
- 4b. El sistema muestra botón de WhatsApp
- 4c. El mensaje incluye: folio, modelo, costos y saldo

**Flujo Alternativo 2: Orden Entregada**
- 4a. El estatus es "Entregado"
- 4b. El sistema muestra información de garantía
- 4c. Indica fecha de inicio de garantía (30 días)

**Postcondiciones:**
- El usuario visualiza toda la información de la orden

---

### CU-05: Actualizar Estatus de Orden

**Actor:** Administrador, Técnico

**Descripción:** Cambiar el estatus de una orden según su progreso.

**Precondiciones:**
- El usuario debe estar autenticado
- La orden debe existir en el sistema

**Flujo Principal:**
1. El usuario accede al detalle de una orden
2. El sistema muestra el estatus actual
3. El usuario selecciona un nuevo estatus del dropdown:
   - Recibido
   - En Proceso
   - Listo
   - Entregado
4. El usuario hace clic en "Actualizar Estatus"
5. El sistema actualiza el estatus en la base de datos
6. El sistema recarga la página con el nuevo estatus

**Flujo Alternativo 1: Cambio a "Entregado"**
- 3a. El usuario selecciona "Entregado"
- 5a. El sistema registra la fecha de entrega automáticamente
- 5b. El sistema activa el período de garantía

**Postcondiciones:**
- El estatus de la orden se actualiza
- Si es "Entregado", se registra fecha de entrega

**Reglas de Negocio:**
- Cualquier estatus puede cambiar a cualquier otro
- Solo "Entregado" registra fecha de entrega
- La garantía inicia desde la fecha de entrega

---

### CU-06: Generar Código QR de Orden

**Actor:** Administrador, Técnico

**Descripción:** Generar código QR con información de la orden para etiqueta física.

**Precondiciones:**
- El usuario debe estar autenticado
- La orden debe existir en el sistema

**Flujo Principal:**
1. El usuario accede al detalle de una orden
2. El sistema genera automáticamente un código QR que contiene:
   - Nombre del taller
   - Folio de la orden
   - Nombre del cliente
   - Marca y modelo del equipo
3. El sistema muestra el código QR en pantalla
4. El usuario puede hacer clic en "Imprimir QR"
5. El navegador abre diálogo de impresión
6. El usuario imprime la etiqueta

**Postcondiciones:**
- Se genera código QR visible
- El usuario puede imprimir etiqueta física

**Datos en el QR:**
```
Taller Felinormar
Folio: FN-0001
Cliente: Juan Pérez
Equipo: Samsung Galaxy S21
```

---

### CU-07: Enviar Notificación WhatsApp

**Actor:** Administrador, Técnico

**Descripción:** Notificar al cliente que su equipo está listo para recoger.

**Precondiciones:**
- El usuario debe estar autenticado
- La orden debe tener estatus "Listo"
- El cliente debe tener teléfono registrado

**Flujo Principal:**
1. El usuario accede al detalle de una orden con estatus "Listo"
2. El sistema muestra botón "Notificar por WhatsApp"
3. El usuario hace clic en el botón
4. El sistema genera mensaje pre-llenado:
   - Saludo personalizado con nombre del cliente
   - Folio de la orden
   - Modelo del equipo
   - Costo total
   - Anticipo pagado
   - Saldo pendiente
5. El sistema abre WhatsApp Web/App con el mensaje
6. El usuario puede editar el mensaje si lo desea
7. El usuario envía el mensaje desde WhatsApp

**Mensaje Generado:**
```
¡Hola Juan! 📱 Su equipo Samsung Galaxy S21 con folio FN-0001 
ya está listo para recoger en Taller Felinormar. 
Costo total: $850.00 | Anticipo: $400.00 | 
Saldo pendiente: $450.00. ¡Le esperamos! 🔧
```

**Postcondiciones:**
- Se abre WhatsApp con mensaje pre-llenado
- El usuario puede enviar la notificación

---

### CU-08: Ver Dashboard Analítico

**Actor:** Administrador, Técnico

**Descripción:** Visualizar estadísticas y gráficas del negocio.

**Precondiciones:**
- El usuario debe estar autenticado

**Flujo Principal:**
1. El usuario hace clic en "Dashboard" en el menú
2. El sistema muestra KPIs principales:
   - Total de órdenes registradas
   - Ingresos totales (órdenes entregadas)
   - Órdenes pendientes de entrega
3. El sistema muestra gráfica de "Top 5 Modelos":
   - Gráfica de barras horizontales
   - Muestra los 5 modelos más frecuentes
4. El sistema muestra gráfica de "Ingresos":
   - Gráfica de línea
   - Filtrable por: Semana / Mes / Año
   - Muestra ingresos de órdenes entregadas
5. El sistema muestra gráfica de "Distribución por Estatus":
   - Gráfica de dona
   - Muestra cantidad por cada estatus

**Flujo Alternativo 1: Cambiar Período de Ingresos**
- 4a. El usuario selecciona "Semana", "Mes" o "Año"
- 4b. El sistema recarga la gráfica con datos del período

**Postcondiciones:**
- El usuario visualiza estadísticas actualizadas

**Tecnología:**
- Chart.js para renderizado de gráficas
- API REST JSON para obtener datos

---

### CU-09: Crear Usuario

**Actor:** Administrador

**Descripción:** Registrar un nuevo usuario en el sistema.

**Precondiciones:**
- El usuario debe ser administrador
- El usuario debe estar autenticado

**Flujo Principal:**
1. El administrador hace clic en "Usuarios" en el menú
2. El sistema muestra lista de usuarios existentes
3. El administrador hace clic en "Nuevo Usuario"
4. El sistema muestra formulario de registro
5. El administrador ingresa:
   - Nombre de usuario (único)
   - Contraseña
   - Rol (Admin o Técnico)
6. El administrador hace clic en "Crear Usuario"
7. El sistema valida que el usuario no exista
8. El sistema hashea la contraseña (PBKDF2-SHA256)
9. El sistema guarda el nuevo usuario
10. El sistema redirige a la lista de usuarios

**Flujo Alternativo 1: Usuario Duplicado**
- 7a. El nombre de usuario ya existe
- 7b. El sistema muestra mensaje de error
- 7c. El administrador debe elegir otro nombre

**Postcondiciones:**
- Se crea un nuevo usuario en el sistema
- La contraseña se almacena hasheada
- El usuario puede iniciar sesión

**Reglas de Negocio:**
- Los nombres de usuario deben ser únicos
- Las contraseñas se almacenan hasheadas
- Solo administradores pueden crear usuarios

---

### CU-10: Eliminar Usuario

**Actor:** Administrador

**Descripción:** Eliminar un usuario del sistema.

**Precondiciones:**
- El usuario debe ser administrador
- El usuario debe estar autenticado
- El usuario a eliminar no debe ser "admin"

**Flujo Principal:**
1. El administrador accede a "Usuarios"
2. El sistema muestra lista de usuarios
3. El administrador hace clic en "Eliminar" de un usuario
4. El sistema elimina el usuario de la base de datos
5. El sistema redirige a la lista actualizada

**Reglas de Negocio:**
- No se puede eliminar el usuario "admin"
- No hay confirmación (acción directa)

**Postcondiciones:**
- El usuario es eliminado del sistema
- El usuario no puede iniciar sesión

---

### CU-11: Gestionar Catálogo de Reparaciones

**Actor:** Administrador

**Descripción:** Administrar el catálogo de servicios y sus costos.

**Precondiciones:**
- El usuario debe ser administrador
- El usuario debe estar autenticado

**Flujo Principal:**
1. El administrador hace clic en "Catálogo" en el menú
2. El sistema muestra lista de reparaciones:
   - Descripción del servicio
   - Costo estándar
3. El administrador puede agregar nueva reparación:
   - Ingresa descripción
   - Ingresa costo
   - Hace clic en "Agregar"
4. El sistema guarda la nueva reparación
5. El administrador puede eliminar reparaciones existentes

**Postcondiciones:**
- El catálogo se actualiza
- Las nuevas reparaciones están disponibles al crear órdenes

---

### CU-12: Cerrar Sesión

**Actor:** Administrador, Técnico

**Descripción:** Finalizar la sesión del usuario.

**Precondiciones:**
- El usuario debe estar autenticado

**Flujo Principal:**
1. El usuario hace clic en "Cerrar sesión"
2. El sistema destruye la sesión del usuario
3. El sistema redirige a la pantalla de login

**Postcondiciones:**
- La sesión del usuario se cierra
- El usuario debe autenticarse nuevamente para acceder

---

## Flujos de Trabajo

### Flujo 1: Recepción de Equipo

```
1. Cliente llega al taller con equipo dañado
   ↓
2. Técnico crea nueva orden (CU-02)
   - Registra datos del cliente
   - Registra datos del equipo
   - Describe el problema
   - Selecciona tipo de reparación
   - Registra anticipo
   ↓
3. Sistema genera folio único (FN-XXXX)
   ↓
4. Sistema genera código QR (CU-06)
   ↓
5. Técnico imprime etiqueta QR
   ↓
6. Técnico entrega comprobante al cliente
   ↓
7. Orden queda con estatus "Recibido"
```

### Flujo 2: Proceso de Reparación

```
1. Técnico consulta órdenes pendientes (CU-03)
   ↓
2. Técnico selecciona orden a reparar
   ↓
3. Técnico actualiza estatus a "En Proceso" (CU-05)
   ↓
4. Técnico realiza la reparación física
   ↓
5. Técnico actualiza estatus a "Listo" (CU-05)
   ↓
6. Sistema habilita botón de WhatsApp
```

### Flujo 3: Notificación y Entrega

```
1. Orden tiene estatus "Listo"
   ↓
2. Técnico accede al detalle de la orden (CU-04)
   ↓
3. Técnico hace clic en "Notificar por WhatsApp" (CU-07)
   ↓
4. Sistema genera mensaje con:
   - Nombre del cliente
   - Folio
   - Modelo
   - Costos y saldo
   ↓
5. Técnico envía mensaje por WhatsApp
   ↓
6. Cliente llega a recoger equipo
   ↓
7. Técnico cobra saldo pendiente
   ↓
8. Técnico actualiza estatus a "Entregado" (CU-05)
   ↓
9. Sistema registra fecha de entrega
   ↓
10. Sistema activa garantía de 30 días
```

### Flujo 4: Análisis de Negocio

```
1. Administrador accede al Dashboard (CU-08)
   ↓
2. Sistema muestra KPIs:
   - Total de órdenes
   - Ingresos totales
   - Pendientes
   ↓
3. Administrador revisa Top 5 Modelos
   - Identifica equipos más frecuentes
   ↓
4. Administrador revisa gráfica de Ingresos
   - Selecciona período (Semana/Mes/Año)
   - Analiza tendencias
   ↓
5. Administrador revisa distribución por estatus
   - Identifica cuellos de botella
   ↓
6. Administrador toma decisiones de negocio
```

---

## Diagramas de Secuencia

### Secuencia: Crear Nueva Orden

```
Usuario          Sistema          Base de Datos
  |                |                    |
  |--Nueva Orden-->|                    |
  |                |                    |
  |<--Formulario---|                    |
  |                |                    |
  |--Datos-------->|                    |
  |                |--Generar Folio---->|
  |                |                    |
  |                |<--Folio Único------|
  |                |                    |
  |                |--Guardar Orden---->|
  |                |                    |
  |                |<--Confirmación-----|
  |                |                    |
  |<--Detalle------|                    |
  |   Orden        |                    |
```

### Secuencia: Notificación WhatsApp

```
Usuario          Sistema          WhatsApp API
  |                |                    |
  |--Ver Detalle-->|                    |
  |                |                    |
  |<--Botón WA-----|                    |
  |                |                    |
  |--Click WA----->|                    |
  |                |--Generar Mensaje-->|
  |                |                    |
  |                |<--URL WhatsApp-----|
  |                |                    |
  |<--Abrir WA-----|                    |
  |                |                    |
  |--Enviar------->|                    |
  |   Mensaje      |                    |
```

### Secuencia: Dashboard Analítico

```
Usuario          Sistema          Base de Datos
  |                |                    |
  |--Dashboard---->|                    |
  |                |                    |
  |                |--Query Stats------>|
  |                |                    |
  |                |<--Datos JSON-------|
  |                |                    |
  |                |--Renderizar------->|
  |                |   Chart.js         |
  |                |                    |
  |<--Gráficas-----|                    |
  |                |                    |
  |--Cambiar------>|                    |
  |   Período      |                    |
  |                |--Query Filtrado--->|
  |                |                    |
  |                |<--Nuevos Datos-----|
  |                |                    |
  |<--Actualizar---|                    |
  |   Gráfica      |                    |
```

---

## Reglas de Negocio

### RN-01: Generación de Folios
- Los folios son únicos y secuenciales
- Formato: FN-XXXX (FN-0001, FN-0002, etc.)
- Se generan automáticamente al crear una orden

### RN-02: Estatus de Órdenes
- Estatus disponibles: Recibido, En Proceso, Listo, Entregado
- Cualquier estatus puede cambiar a cualquier otro
- Solo "Entregado" registra fecha de entrega

### RN-03: Garantía
- La garantía es de 30 días
- Inicia desde la fecha de entrega
- Solo aplica para órdenes con estatus "Entregado"

### RN-04: Notificaciones WhatsApp
- Solo disponible para órdenes con estatus "Listo"
- Requiere teléfono del cliente registrado
- El mensaje incluye información financiera completa

### RN-05: Roles y Permisos
- Admin: Acceso completo al sistema
- Técnico: No puede gestionar usuarios ni catálogo
- Las contraseñas se almacenan hasheadas (PBKDF2-SHA256)

### RN-06: Clientes
- Se identifican por número de teléfono
- Si el teléfono existe, se reutilizan los datos
- Un cliente puede tener múltiples órdenes

### RN-07: Catálogo de Reparaciones
- Solo administradores pueden modificarlo
- Los costos son sugeridos, pueden modificarse por orden
- Las reparaciones eliminadas no afectan órdenes existentes

---

## Métricas y KPIs

### Métricas Operativas
- **Total de órdenes**: Cantidad total de equipos recibidos
- **Órdenes pendientes**: Suma de Recibido + En Proceso + Listo
- **Tasa de entrega**: (Entregados / Total) × 100

### Métricas Financieras
- **Ingresos totales**: Suma de costos de órdenes entregadas
- **Ticket promedio**: Ingresos totales / Órdenes entregadas
- **Anticipo promedio**: Suma de anticipos / Total de órdenes

### Métricas de Producto
- **Top 5 modelos**: Equipos más frecuentes
- **Reparación más común**: Tipo de servicio más solicitado
- **Tiempo promedio**: Días entre ingreso y entrega

---

## Glosario

- **Folio**: Identificador único de una orden (FN-XXXX)
- **Anticipo**: Pago inicial que realiza el cliente
- **Saldo pendiente**: Diferencia entre costo total y anticipo
- **IMEI**: Identificador único de dispositivos móviles
- **QR**: Código de respuesta rápida para identificación
- **Estatus**: Estado actual de una orden en el flujo de trabajo
- **Garantía**: Período de 30 días post-entrega
- **Dashboard**: Panel de control con estadísticas
- **KPI**: Indicador clave de rendimiento (Key Performance Indicator)

---

**Versión:** 1.0  
**Fecha:** 2026-03-12  
**Autor:** Sistema Taller Felinormar
