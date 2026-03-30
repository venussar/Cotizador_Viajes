# Resumen detallado de cambios — Vista de Cotizaciones

## 1. SQL — Nuevas columnas en tabla `quotes`

Se agregaron **4 columnas** a la tabla existente `quotes` para guardar los valores calculados:

```sql
ALTER TABLE quotes
  ADD COLUMN fuel_price DECIMAL(10,2) DEFAULT 0,      -- Precio del galón al momento de cotizar
  ADD COLUMN subtotal DECIMAL(10,2) DEFAULT 0,         -- Suma de todos los costos antes de comisión
  ADD COLUMN commission_value DECIMAL(10,2) DEFAULT 0,  -- Monto $ de la comisión
  ADD COLUMN total DECIMAL(10,2) DEFAULT 0;             -- Total final (subtotal + comisión)
```
---

## 2. `src/models/entities/quote.py` — Entidad Quote

**Antes:** 9 propiedades (id, round_trip_distance_km, tolls_value, incentive_value, hotel_cost, commission_percentage, vehicle_id, user_id, created_at)

**Después:** 15 propiedades. Se agregaron:
- `fuel_price` — precio combustible guardado
- `subtotal` — subtotal calculado
- `commission_value` — valor de la comisión en $
- `total` — total final
- `vehicle_name` — nombre del vehículo (viene del JOIN, no se guarda en quotes)
- `username` — nombre del usuario (viene del JOIN, no se guarda en quotes)

Los nuevos parámetros tienen valores por defecto para no romper código existente.

---

## 3. `src/models/modelquote.py` — ModelQuote

### Método `get_all_by_user()`

**Antes:**
```sql
SELECT id, round_trip_distance_km, tolls_value,
       incentive_value, hotel_cost, commission_percentage,
       vehicle_id, user_id, created_at
FROM quotes WHERE user_id = %s
```

**Después:**
```sql
SELECT q.id, q.round_trip_distance_km, q.tolls_value,
       q.incentive_value, q.hotel_cost, q.commission_percentage,
       q.vehicle_id, q.user_id, q.created_at,
       q.fuel_price, q.subtotal, q.commission_value, q.total,
       v.type_vehicles, u.namee
FROM quotes q
LEFT JOIN vehicles v ON q.vehicle_id = v.id
LEFT JOIN users u ON q.user_id = u.id
WHERE q.user_id = %s
ORDER BY created_at DESC
```

**Cambios:**
- Se agregaron las 4 nuevas columnas de quotes
- Se hace **LEFT JOIN** con `vehicles` para traer `type_vehicles` (nombre del vehículo)
- Se hace **LEFT JOIN** con `users` para traer `namee` (nombre del usuario)
- Así el historial ya tiene todo en una sola consulta sin necesidad de queries adicionales

### Método `create()`

**Antes:** Insertaba 7 valores (round_trip_distance_km, tolls_value, incentive_value, hotel_cost, commission_percentage, vehicle_id, user_id)

**Después:** Inserta **11 valores** — los 7 originales + fuel_price, subtotal, commission_value, total

---

## 4. `src/templates/qoutes/cotizaciones.html` — Formulario de cotización

### A) Select de vehículos — data-attributes

**Antes:**
```html
<option value="{{ vehiculo.id }}">{{ vehiculo.type_vehicles }}</option>
```

**Después:**
```html
<option value="{{ vehiculo.id }}"
    data-fuel="{{ vehiculo.fuel_consumption_km }}"
    data-driver="{{ vehiculo.driver_cost }}"
    data-labor="{{ vehiculo.labor_cost }}">
    {{ vehiculo.type_vehicles }}
</option>
```

Cada opción ahora lleva los datos del vehículo como `data-*` attributes para que el JavaScript los lea sin hacer otra petición al servidor.

### B) Hidden inputs — antes del botón guardar

Se agregaron 3 campos ocultos:
```html
<input type="hidden" name="subtotal_hidden" id="hiddenSubtotal">
<input type="hidden" name="commission_value_hidden" id="hiddenCommissionValue">
<input type="hidden" name="total_hidden" id="hiddenTotal">
```

Estos se llenan automáticamente con JS cuando cambian los valores y se envían con el formulario.

### C) JavaScript — cálculo completo reescrito

**Antes:**
- No usaba datos del vehículo
- `costoCombustible = distancia × precioCombustible` (incorrecto)
- Conductor y Mano de Obra siempre mostraban $0.00
- No enviaba totales al backend

**Después:**
- Nueva función `getVehicleData()` que lee `data-fuel`, `data-driver`, `data-labor` del option seleccionado
- Fórmula correcta: `costoCombustible = (distancia / fuel_consumption_km) × precioCombustible`
- Conductor y Mano de Obra se llenan con los valores del vehículo
- `subtotal = combustible + peajes + incentivos + hotel + conductor + manoObra`
- `comisión = subtotal × porcentaje / 100`
- `total = subtotal + comisión`
- Al cambiar el select de vehículo se recalcula todo (`change` event)
- Los hidden inputs se actualizan automáticamente en cada recálculo

---

## 5. `src/controllers/qoute_controller.py` — Controller

### Ruta `/historial` (GET)

**Antes:**
```python
def historial():
    return render_template('qoutes/historial.html')
```

**Después:**
```python
def historial():
    from app import db
    cotizaciones = ModelQuote.get_all_by_user(db, current_user.id)
    return render_template('qoutes/historial.html', cotizaciones=cotizaciones)
```

Ahora consulta las cotizaciones del usuario logueado y las envía al template.

### Ruta `/cotizaciones/crear` (POST)

**Antes:** El dict `data` tenía 7 campos. `precio_combustible` se extraía pero nunca se usaba.

**Después:** El dict `data` tiene **11 campos**. Se agregaron:
```python
"fuel_price": float(precio_combustible),
"subtotal": float(request.form.get('subtotal_hidden', 0)),
"commission_value": float(request.form.get('commission_value_hidden', 0)),
"total": float(request.form.get('total_hidden', 0)),
```

---

## 6. `src/templates/qoutes/historial.html` — Vista del historial

**Antes:** Solo tenía `<thead>` — sin `<tbody>`, no mostraba datos.

**Después:** Se completó con:
- `<tbody>` con un `{% for cot in cotizaciones %}` que recorre las cotizaciones
- Cada fila muestra: **ID + fecha**, **nombre del vehículo**, **distancia en km**, **nombre del usuario**, **total formateado**, y un **botón de detalle**
- Si no hay cotizaciones, muestra un mensaje "No hay cotizaciones registradas aún."
- Botón de detalle con `verDetalle(id)` (placeholder por ahora)

---

## Flujo completo

```
1. Usuario entra a /cotizaciones
2. Selecciona vehículo → JS carga fuel_consumption, driver_cost, labor_cost
3. Llena distancia, precio combustible, peajes, incentivos, hotel
4. JS calcula todo en tiempo real y lo muestra en el panel derecho
5. Click "Guardar" → se envían datos del form + hidden inputs (subtotal, comisión, total)
6. Backend guarda todo en quotes (incluyendo fuel_price, subtotal, commission_value, total)
7. Usuario va a /historial → ve todas sus cotizaciones con vehículo, distancia, total y fecha
```

---

## 7. Formato de moneda — Pesos colombianos (COP)

### Cambio en JavaScript (`cotizaciones.html`)

Se agregó la función `formatCOP()` para mostrar valores en formato de pesos colombianos:

```javascript
function formatCOP(valor) {
    return '$' + valor.toLocaleString('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
```

**Antes:** Los valores se mostraban como `$1265000.00` (formato americano)

**Después:** Los valores se muestran como `$1.265.000,00` (formato colombiano — punto para miles, coma para decimales)

### Campos actualizados:
- Combustible, Peajes, Conductor, Mano de Obra, Hotel, Incentivos
- Subtotal, Comisión, Total General

### Valores iniciales en HTML:
Todos los valores por defecto cambiaron de `$0.00` a `$0,00` para mantener consistencia visual antes de que el JS calcule.

### Elemento eliminado:
Se removió la badge `<span class="comision-valor" id="comisionDisplay">15%</span>` del slider de comisión (el porcentaje ya se muestra en el panel de desglose).

---

## 8. Formato de miles en campos de entrada + sin decimales

### Cambios en inputs del formulario

**Antes:** Los inputs eran `type="number"` y mostraban números planos (`50000`, `20000`).

**Después:** Los inputs son `type="text"` con clase `formato-miles` y muestran separador de miles al escribir (`50.000`, `20.000`). Se usa `inputmode="numeric"` para que en móviles aparezca el teclado numérico.

Cada input visible tiene un `<input type="hidden">` asociado (ej: `id="distancia_raw"`) que almacena el valor numérico puro para enviarlo al backend.

### Nuevas funciones JavaScript

```javascript
// Formatear input con separador de miles y sincronizar hidden
function formatearInputMiles(input) {
    const raw = input.value.replace(/\./g, '').replace(/[^0-9]/g, '');
    const numero = parseInt(raw) || 0;
    input.value = numero > 0 ? numero.toLocaleString('es-CO') : '';
    const hidden = document.getElementById(input.id + '_raw');
    if (hidden) hidden.value = numero;
}

// Obtener valor numérico de un input formateado
function getValor(input) {
    return parseInt(input.value.replace(/\./g, '').replace(/[^0-9]/g, '')) || 0;
}
```

- `formatearInputMiles()`: quita puntos y caracteres no numéricos, formatea con `toLocaleString('es-CO')` y sincroniza el hidden.
- `getValor()`: extrae el número puro del input formateado para usarlo en los cálculos.
- Se usa `document.querySelectorAll('.formato-miles')` para aplicar evento `input` a todos los campos de forma automática.

### Sin decimales

`formatCOP()` cambió de `minimumFractionDigits: 2` a `minimumFractionDigits: 0` para que el panel de desglose tampoco muestre decimales. Los valores iniciales en el HTML cambiaron de `$0,00` a `$0`.

### Eventos de cálculo

Los listeners `addEventListener('input', calcularCostos)` de los 5 inputs se eliminaron del bloque final porque ahora el recálculo ocurre dentro del evento del `.formato-miles`. Solo quedan los listeners del select de vehículo y el slider de comisión.

---

## 9. Módulo de Usuarios — CRUD completo

### SQL necesario

```sql
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'cotizador';
```

Se agrega la columna `role` para manejar permisos (cotizador/admin).

---

### 9.1 `src/models/entities/user.py` — Entidad User

**Antes:** 4 propiedades (id, namee, email, password_hash)

**Después:** 5 propiedades. Se agregó:
- `role` — rol del usuario con valor por defecto `'cotizador'`

```python
def __init__(self, id, namee, email, password_hash, role='cotizador'):
```

---

### 9.2 `src/models/modelUser.py` — ModelUser

**Método `create_user()` actualizado:**
- Ahora recibe parámetro `role` (default `'cotizador'`)
- El INSERT incluye la columna `role`

**Método `get_all()` actualizado:**
- Ahora selecciona `id, namee, email, role` (antes no traía `role`)

**Nuevos métodos:**

```python
@staticmethod
def update_user(db, user_id, name, email, role, password=None):
```
- Actualiza nombre, email y rol
- Si se pasa contraseña, también la actualiza (con hash)
- Si no se pasa contraseña, no la toca

```python
@staticmethod
def delete_user(db, user_id):
```
- Elimina un usuario por ID

**Fix en `create_user()`:**
- Se corrigió `` ` password_hash` `` (con backtick y espacio) a `password_hash` (sin backtick) en el INSERT

---

### 9.3 `src/controllers/user_controller.py` — Controller

**Antes:** 1 sola ruta (`/users/create` GET/POST) sin `@login_required`

**Después:** 4 rutas, todas con `@login_required`:

| Ruta | Método | Función |
|---|---|---|
| `/users` | GET | `list_users()` — lista todos los usuarios |
| `/users/create` | GET/POST | `create_user()` — formulario + crear |
| `/users/edit/<id>` | GET/POST | `edit_user()` — formulario pre-llenado + actualizar |
| `/users/delete/<id>` | POST | `delete_user()` — eliminar con confirmación |

**Validaciones en crear y editar:**
- Contraseñas deben coincidir
- Mínimo 6 caracteres
- En editar, la contraseña es opcional (dejar vacío = no cambia)

**Fix del error anterior:**
- Si hay error al crear, redirige a `create_user` (no a `list_users`)
- Así el flash de error se muestra en el formulario correcto

---

### 9.4 `src/templates/users/create_user.html` — Rediseño

**Antes:** Formulario básico sin estilo, 3 campos (nombre con `name="name"` — bug), sin validación

**Después:**
- Diseño con card y encabezado, consistente con el resto de la app
- Layout en 2 columnas (nombre + email, contraseña + confirmar)
- Iconos en los inputs: 👤 persona, ✉ correo, 🔒 candado, ⚙ rol
- Campo `name="namee"` corregido (antes era `name="name"`, no coincidía con el controller)
- Campo "Confirmar Contraseña" nuevo
- Selector de Rol (Cotizador / Administrador)
- Botón "Volver a la lista"
- `minlength="6"` en campos de contraseña

---

### 9.5 `src/templates/users/list_users.html` — NUEVO

Tabla con todos los usuarios:
- Encabezado con título "Gestión de Usuarios" y botón "+ Nuevo Usuario"
- Contador de usuarios en el header del card
- Columnas: ID, Nombre (con icono 👤), Correo, Rol, Acciones
- **Badges de rol**: rojo "Admin" / azul "Cotizador"
- **Botón editar**: ✏ enlace a `/users/edit/<id>`
- **Botón eliminar**: 🗑 formulario POST con `confirm()` de JavaScript
- Mensaje empty state si no hay usuarios

---

### 9.6 `src/templates/users/edit_user.html` — NUEVO

Formulario de edición:
- Misma estructura y estilo que `create_user.html`
- Campos pre-llenados con `value="{{ user.namee }}"`, `value="{{ user.email }}"`
- Select de rol con `selected` dinámico según el rol actual
- Contraseña **opcional**: texto "(dejar vacío para no cambiar)"
- Botón "Volver a la lista"

---

### 9.7 `src/static/css/usuarios.css` — NUEVO

Estilos para el módulo:
- `.usuario-card` — card con max-width 700px, bordes redondeados
- `.input-group-text` — fondo claro para los iconos
- `.usuarios-table` — headers en uppercase, hover en filas
- `.badge` — estilo para las badges de rol
- Responsive: card al 100% en móvil, tabla con font-size reducido

---

### 9.8 `src/templates/base.html` — Flash messages globales

**Cambio:** Se agregó bloque de flash messages entre el nav y el contenido:

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }} alert-dismissible fade show">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

Ahora los mensajes flash funcionan en **todas las vistas** (antes solo login y vehículos lo manejaban individualmente).

El link de "Usuarios" en la navbar cambió de `url_for('user.create_user')` a `url_for('user.list_users')`.

---

### 9.9 `src/controllers/auth_controller.py` — Ruta duplicada eliminada

**Se eliminó** la ruta `/users` de `auth_controller.py`:

```python
# ELIMINADO:
@auth_bp.route('/users', methods=['GET'])
def list_users():
    try:
        users = ModelUser.get_all(db)  # ← 'db' no estaba importado
        return render_template('auth/users.html', users=users)
    except Exception as ex:
        return str(ex)  # ← devolvía error como texto plano
```

Esta ruta era la causa del error **"name 'db' is not defined"** — no importaba `db` y el `except` devolvía el error como texto plano sin template. Al estar en `auth_bp` se registraba antes que la de `user_bp`, interceptando las peticiones a `/users`.
