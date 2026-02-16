# Documentacion Tecnica - Project Hub

## Tabla de Contenidos

1. [Arquitectura General](#1-arquitectura-general)
2. [Estructura de Archivos](#2-estructura-de-archivos)
3. [Diagrama Entidad-Relacion](#3-diagrama-entidad-relacion)
4. [Modelos de Base de Datos](#4-modelos-de-base-de-datos)
5. [Rutas y Endpoints](#5-rutas-y-endpoints)
6. [Estructura HTML y Etiquetas Semanticas](#6-estructura-html-y-etiquetas-semanticas)
7. [Renderizado Dinamico de Templates](#7-renderizado-dinamico-de-templates)
8. [Sistema de Autorizacion](#8-sistema-de-autorizacion)

---

## 1. Arquitectura General

Project Hub sigue el patron **MVC (Model-View-Controller)** con una capa de servicios adicional:

```
                    PETICION HTTP
                         |
                         v
                  +-------------+
                  |   Routes    |  <-- Controladores (Blueprints de Flask)
                  +-------------+
                   /           \
                  v             v
          +-----------+   +------------+
          | Services  |   | Templates  |  <-- Vista (Jinja2)
          +-----------+   +------------+
               |
               v
          +-----------+
          |  Models   |  <-- Modelo (SQLAlchemy ORM)
          +-----------+
               |
               v
          +-----------+
          |  SQLite   |  <-- Base de datos
          +-----------+
```

### Capas de la aplicacion

| Capa | Directorio | Responsabilidad |
|------|-----------|-----------------|
| **Controlador** | `routes/` | Recibe peticiones HTTP, valida datos, llama servicios y retorna respuestas |
| **Servicio** | `services/` | Logica de negocio: operaciones CRUD, validaciones complejas |
| **Modelo** | `models/` | Definicion de tablas con SQLAlchemy ORM, relaciones entre entidades |
| **Vista** | `templates/` | Plantillas Jinja2 que generan el HTML final |
| **Utilidades** | `utils/` | Decoradores de autorizacion, funciones de seed |

### Stack tecnologico

- **Backend:** Python 3.8+ con Flask 3.1.2
- **ORM:** SQLAlchemy 2.0 via Flask-SQLAlchemy 3.1.1
- **Base de datos:** SQLite 3 (archivo `instance/projecthub.db`)
- **Motor de plantillas:** Jinja2 3.1.6
- **Frontend:** HTML5 semantico + CSS3 + JavaScript vanilla
- **Hashing de contrasenas:** Werkzeug (generate_password_hash / check_password_hash)

---

## 2. Estructura de Archivos

```
project-hub/
|
|-- 🐍 app.py                        # Fabrica de la aplicacion Flask (create_app)
|-- 🐍 index.py                      # Punto de entrada: ejecuta app.run()
|-- 📄 requirements.txt              # Dependencias de Python
|-- 📄 LICENSE                       # Licencia MIT
|-- 📝 README.md                     # Documentacion de usuario
|
|-- 📁 docs
│   +-- 📁 screenshots 
|
|-- 📁 instance
|   +-- projecthub.db                # Base de datos SQLite (se genera automaticamente)
|
├── 📁 models                        # Modelos de la base de datos
|   |-- 🐍 __init__.py               # Exporta db y todos los modelos
|   |-- 🐍 user.py                   # Modelo User + enum de roles
|   |-- 🐍 call.py                   # Modelo Call (convocatoria)
|   |-- 🐍 project.py                # Modelo Project
|   +-- 🐍 deliverable.py            # Modelo Deliverable (archivos)
|
|-- 📁 routes                        # Controladores (Flask Blueprints)
│   ├── 📝 README.md
|   |-- 🐍 __init__.py               # Exporta todos los blueprints
|   |-- 🐍 auth_routes.py            # Registro, login, logout
|   |-- 🐍 user_routes.py            # CRUD de usuarios (admin/owner)
|   |-- 🐍 call_routes.py            # CRUD de convocatorias
|   |-- 🐍 project_routes.py         # CRUD de proyectos
|   +-- 🐍 deliverable_routes.py     # Subida, descarga y gestion de archivos
|
|-- 📁 services                      # Logica de negocio
│   ├── 📝 README.md
|   |-- 🐍 auth_service.py           # Autenticacion (registro/login)
|   |-- 🐍 user_service.py           # Operaciones CRUD de usuarios
|   |-- 🐍 call_service.py           # Operaciones CRUD de convocatorias
|   |-- 🐍 project_service.py        # Operaciones CRUD de proyectos
|   +-- 🐍 deliverable_service.py    # Manejo de archivos
|
|-- 📁 utils                         # Utilidades
│   ├── 📝 README.md
|   |-- 🐍 decorators.py             # Decoradores: login_required, admin_required, owner_required
|   +-- 🐍 seed.py                   # Datos iniciales para la base de datos
|
|-- 📁 templates                     # Plantillas Jinja2
|   |-- 🌐 base.html                  # Plantilla base (sidebar, header, footer)
|   |-- 🌐 home.html                  # Pagina de inicio
|   |-- 📁 auth 
|   |   |-- 🌐 login.html             # Formulario de login
|   |   +-- 🌐 register.html          # Formulario de registro
|   |-- 📁 admin 
|   |   |-- 🌐 manage_admin.html      # Gestion de administradores (solo owner)
|   |   +-- 🌐 manage_user.html       # Gestion de lideres (admin/owner)
|   |-- 📁 call 
|   |   |-- 🌐 manage_call.html       # Listado y gestion de convocatorias
|   |   +-- 🌐 view_call.html         # Detalle de una convocatoria
|   |-- 📁 project 
|   |   |-- 🌐 manage_project.html    # Listado y gestion de proyectos
|   |   +-- 🌐 view_project.html      # Detalle de un proyecto con sus archivos
|   +-- 📁 partials 
|       |-- 🌐 _confirm_modal.html    # Modal reutilizable de confirmacion
|       |-- 🌐 _user_table.html       # Tabla reutilizable de usuarios
|       |-- 🌐 _user_form_modal.html  # Modal de creacion de usuario
|       +-- 🌐 _user_edit_modal.html  # Modal de edicion de usuario
|
+-- 📁 static                       # Archivos estaticos
    |-- 📁 css 
    |   +-- 🎨 styles.css           # Hoja de estilos principal
    |-- 📁 js 
    |   |-- 📄 call-actions.js      # Logica de formularios de convocatorias
    |   |-- 📄 error-handler.js     # Manejo global de errores (modal)
    |   |-- 📄 form-validation.js   # Validacion de formularios del lado del cliente
    |   |-- 📄 project-actions.js   # Logica de formularios de proyectos
    |   |-- 📄 toggle-password.js   # Toggle de visibilidad de contrasena
    |   +-- 📄 user-actions.js      # Operaciones CRUD de usuarios (AJAX)
    |-- 📁 images
    |   +-- 📁 logo
    |       |-- 📄 logo.ico         # Favicon
    |       +-- 🖼️ logo.png         # Logo de la aplicacion
    +-- 📁 uploads                  # Almacenamiento de archivos subidos
```

---

## 3. Diagrama Entidad-Relacion

```
+========================+          +========================+
|         users          |          |         calls          |
+========================+          +========================+
| PK  id           INT   |         | PK  id           INT   |
|     enrollment   STR(10)|         |     title        STR(80)|  << UNIQUE, NOCASE
|       _number          |         |     description  TEXT   |
|     name         STR(80)|         |     opening_date DATETIME|
|     password     STR   |         |     closing_date DATETIME|
|       _hash      (128) |         |     created_at   DATETIME|
|     role         ENUM  |         |                        |
|       (owner/admin/    |         |  @property is_active:  |
|        leader)         |         |  opening <= now <=     |
|     created_at   DATETIME|        |  closing               |
+========================+          +========================+
         |  1                                  |  1
         |                                     |
         |  tiene muchos                       |  tiene muchos
         |                                     |
         |  N                                  |  N
         v                                     v
+===================================================+
|                     projects                       |
+===================================================+
| PK  id              INT                            |
|     name            STR(80)                        |
|     description     TEXT                           |
| FK  leader_id       INT  ------>  users.id         |
| FK  call_id         INT  ------>  calls.id         |
|     is_public       BOOL (default: false)          |
|     created_at      DATETIME                       |
+===================================================+
                        |  1
                        |
                        |  tiene muchos
                        |
                        |  N
                        v
         +============================+
         |       deliverables         |
         +============================+
         | PK  id            INT      |
         |     name          STR(80)  |  << UNIQUE, NOCASE
         |     description   TEXT     |
         |     file_path     STR(255) |
         | FK  project_id    INT --------->  projects.id
         |     is_public     BOOL     |  (default: false)
         |     created_at    DATETIME |
         +============================+
```

### Relaciones

```
users  1 ----< N  projects      Un usuario (leader) puede tener muchos proyectos
calls  1 ----< N  projects      Una convocatoria puede tener muchos proyectos
projects 1 --< N  deliverables  Un proyecto puede tener muchos archivos
```

### Restricciones importantes

- `users.enrollment_number` es UNIQUE e indexado (para busquedas rapidas en login)
- `calls.title` es UNIQUE con collation NOCASE (no distingue mayusculas)
- `deliverables.name` es UNIQUE con collation NOCASE
- `projects.leader_id` y `projects.call_id` son Foreign Keys obligatorias
- `deliverables.project_id` es Foreign Key obligatoria

---

## 4. Modelos de Base de Datos

### User (`models/user.py`)

```python
class RoleEnum(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    LEADER = "leader"

class User(db.Model):
    __tablename__ = "users"
    id               # Integer, PK
    enrollment_number  # String(10), UNIQUE, INDEX
    name             # String(80)
    password_hash    # String(128)
    role             # Enum(RoleEnum), default=LEADER
    created_at       # DateTime, default=utcnow
```

- Las contrasenas se hashean con `werkzeug.security.generate_password_hash()`
- Se verifican con `werkzeug.security.check_password_hash()`

### Call (`models/call.py`)

```python
class Call(db.Model):
    __tablename__ = "calls"
    id              # Integer, PK
    title           # String(80), UNIQUE, NOCASE
    description     # Text, nullable
    opening_date    # DateTime
    closing_date    # DateTime
    created_at      # DateTime, default=utcnow
```

- Tiene una propiedad calculada `is_active`: retorna `True` si la fecha actual esta entre `opening_date` y `closing_date`
- Relacion: `projects` (backref desde Project)

### Project (`models/project.py`)

```python
class Project(db.Model):
    __tablename__ = "projects"
    id              # Integer, PK
    name            # String(80)
    description     # Text, nullable
    leader_id       # Integer, FK -> users.id
    call_id         # Integer, FK -> calls.id
    is_public       # Boolean, default=False
    created_at      # DateTime, default=utcnow
```

- Relaciones: `leader` (User), `call` (Call), `deliverables` (backref desde Deliverable)

### Deliverable (`models/deliverable.py`)

```python
class Deliverable(db.Model):
    __tablename__ = "deliverables"
    id              # Integer, PK
    name            # String(80), UNIQUE, NOCASE
    description     # Text
    file_path       # String(255) - ruta en static/uploads/
    project_id      # Integer, FK -> projects.id
    is_public       # Boolean, default=False
    created_at      # DateTime, default=utcnow
```

---

## 5. Rutas y Endpoints

Todas las funciones de ruta tienen **type hints** en parametros y retorno, y un **comentario descriptivo** antes de cada definicion. Los parametros de URL estan tipados como `int`, y los retornos como `str` (HTML), `Response` (JSON/redirect) o `str | Response` (ambos).

### Funcion auxiliar

```python
# project_routes.py
def _check_call_active(
    project_id: Optional[int] = None, call_id: Optional[int] = None
) -> Optional[tuple[Response, int]]:
```

Retorna error 403 si la convocatoria esta inactiva y el usuario no es admin/owner. Se usa en create, update, delete y toggle_visibility de proyectos y archivos.

### Rutas de la Aplicacion Principal (`app.py`)

| Metodo | Ruta | Accion | Acceso |
|--------|------|--------|--------|
| GET | `/` | Redirige a `/home` | Publico |
| GET | `/home` | Pagina de inicio con proyectos publicos (para leaders) | login_required |

### Autenticacion (`/auth`) - `routes/auth_routes.py`

| Metodo | Ruta | Funcion | Respuesta | Acceso |
|--------|------|---------|-----------|--------|
| GET | `/auth/register` | `register() -> str \| Response` | HTML | Publico |
| POST | `/auth/register` | `register() -> str \| Response` | Redirect | Publico |
| GET | `/auth/login` | `login() -> str \| Response` | HTML | Publico |
| POST | `/auth/login` | `login() -> str \| Response` | Redirect | Publico |
| GET | `/auth/logout` | `logout() -> Response` | Redirect | Publico |

### Gestion de Usuarios (`/user`) - `routes/user_routes.py`

| Metodo | Ruta | Funcion | Respuesta | Acceso |
|--------|------|---------|-----------|--------|
| GET | `/user/manage_admin` | `manage_admin() -> str \| Response` | HTML | owner_required |
| POST | `/user/manage_admin` | `manage_admin() -> str \| Response` | Redirect | owner_required |
| PUT | `/user/admin/<user_id>` | `update_admin(user_id: int) -> Response` | JSON | owner_required |
| DELETE | `/user/admin/<user_id>` | `delete_admin(user_id: int) -> Response` | JSON | owner_required |
| GET | `/user/manage_user` | `manage_user() -> str` | HTML | admin_required |
| PUT | `/user/leader/<user_id>` | `update_leader(user_id: int) -> Response` | JSON | admin_required |
| DELETE | `/user/leader/<user_id>` | `delete_leader(user_id: int) -> Response` | JSON | admin_required |

### Convocatorias (`/call`) - `routes/call_routes.py`

| Metodo | Ruta | Funcion | Respuesta | Acceso |
|--------|------|---------|-----------|--------|
| GET | `/call/` | `view_all() -> str` | HTML | login_required |
| POST | `/call/` | `create_call() -> Response` | JSON (201) | admin_required |
| GET | `/call/<call_id>` | `view_call(call_id: int) -> str` | HTML | login_required |
| PUT | `/call/<call_id>` | `update_call(call_id: int) -> Response` | JSON | admin_required |
| DELETE | `/call/<call_id>` | `delete_call(call_id: int) -> Response` | JSON | admin_required |

### Proyectos (`/project`) - `routes/project_routes.py`

| Metodo | Ruta | Funcion | Respuesta | Acceso |
|--------|------|---------|-----------|--------|
| GET | `/project/` | `view_all() -> str` | HTML | login_required |
| POST | `/project/` | `create_project() -> Response` | JSON (201) | login_required |
| GET | `/project/<project_id>` | `view_project(project_id: int) -> str` | HTML | login_required (*) |
| PUT | `/project/<project_id>` | `update_project(project_id: int) -> Response` | JSON | login_required (*) |
| PATCH | `/project/<project_id>/visibility` | `toggle_visibility(project_id: int) -> Response` | JSON | login_required (*) |
| DELETE | `/project/<project_id>` | `delete_project(project_id: int) -> Response` | JSON | login_required (*) |

> (*) Con verificacion adicional: solo el lider del proyecto o admin/owner pueden modificar. Solo se permite modificar si la convocatoria asociada esta activa (excepto admin/owner).

### Archivos (`/deliverable`) - `routes/deliverable_routes.py`

| Metodo | Ruta | Funcion | Respuesta | Acceso |
|--------|------|---------|-----------|--------|
| GET | `/deliverable/view/<deliverable_id>` | `view_deliverable(deliverable_id: int) -> Response` | Archivo | login_required (*) |
| GET | `/deliverable/download/<deliverable_id>` | `download_deliverable(deliverable_id: int) -> Response` | Archivo | login_required (*) |
| POST | `/deliverable/upload/<project_id>` | `upload_deliverable(project_id: int) -> Response` | JSON (201) | login_required (**) |
| PUT | `/deliverable/<deliverable_id>` | `update_deliverable(deliverable_id: int) -> Response` | JSON | login_required (**) |
| PATCH | `/deliverable/<deliverable_id>/visibility` | `toggle_file_visibility(deliverable_id: int) -> Response` | JSON | login_required (**) |
| DELETE | `/deliverable/<deliverable_id>` | `delete_deliverable(deliverable_id: int) -> Response` | JSON | login_required (***) |

> (*) Puede ver/descargar: admin/owner, el lider del proyecto, o cualquiera si el proyecto Y el archivo son publicos.
> (**) Solo el lider del proyecto puede subir/editar. Requiere convocatoria activa.
> (***) El lider del proyecto o admin/owner pueden eliminar.

### Patron de respuestas

- **Rutas GET que renderizan paginas:** Retornan `str` (HTML) via `render_template()`
- **Rutas POST/PUT/PATCH/DELETE de datos:** Retornan `Response` (JSON) via `jsonify()` (consumidas por JavaScript con `fetch()`)
- **Rutas POST de formularios tradicionales (auth, manage_admin):** Retornan `str | Response` (redirect con `flash()` messages)
- **Errores de validacion:** JSON con codigo 422 y objeto `errors` con campos especificos
- **Errores de autorizacion:** JSON con codigo 403
- **Errores de recurso no encontrado:** JSON con codigo 404
- **Errores internos:** JSON con codigo 500

---

## 6. Estructura HTML y Etiquetas Semanticas

### Plantilla base (`base.html`)

La plantilla base define la estructura general de todas las paginas:

```
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" ...>        <!-- Responsive -->
    <title>{% block title %}</title>   <!-- Titulo dinamico -->
    <link rel="icon" ...>              <!-- Favicon -->
    <link rel="stylesheet" ...>        <!-- CSS -->
  </head>

  <body>
    <!-- Flash Messages (mensajes temporales del servidor) -->
    <!-- Error Modal (errores con imagen de gato HTTP) -->

    {% if usuario_autenticado %}
    <div class="app-layout">

      <aside class="sidebar">           <!-- SEMANTICA: contenido lateral -->
        <div class="sidebar-header">
          <h2>ProjectHub</h2>            <!-- Titulo de la app -->
          <button>toggle</button>        <!-- Colapsar sidebar -->
        </div>

        <nav class="sidebar-nav">       <!-- SEMANTICA: navegacion principal -->
          <a href="/home">Inicio</a>
          <a href="/call/">Convocatorias</a>
          <!-- Links condicionales segun rol -->
        </nav>

        <div class="sidebar-bottom">
          <span>nombre_usuario</span>
          <a href="/auth/logout">Cerrar Sesion</a>
        </div>
      </aside>

      <main class="main-content">       <!-- SEMANTICA: contenido principal -->
        {% block content %}{% endblock %}
      </main>

    </div>
    {% else %}
      {% block content %}{% endblock %}  <!-- Login/Register sin sidebar -->
    {% endif %}

    <footer class="app-footer">          <!-- SEMANTICA: pie de pagina -->
      <p>ProjectHub (c) 2025</p>
    </footer>

    {% block scripts %}{% endblock %}    <!-- JS especifico de cada pagina -->
  </body>
</html>
```

### Etiquetas semanticas HTML5 utilizadas

| Etiqueta | Donde se usa | Proposito |
|----------|-------------|-----------|
| `<aside>` | `base.html` | Barra lateral de navegacion |
| `<nav>` | `base.html` | Agrupacion de enlaces de navegacion |
| `<main>` | `base.html` | Contenido principal de cada pagina |
| `<footer>` | `base.html` | Pie de pagina con copyright |
| `<form>` | Login, register, modales | Formularios de entrada de datos |
| `<table>` | Listados de datos | Tablas con `<thead>`, `<tbody>`, `<th>`, `<td>` |
| `<button>` | Acciones en toda la app | Botones con tipo (`type="submit"`, `type="button"`) |
| `<label>` | Formularios | Etiquetas asociadas a inputs |
| `<input>` | Formularios | Campos de entrada con tipos semanticos (`text`, `password`, `date`, `file`) |
| `<textarea>` | Formularios | Campos de texto largo (descripciones) |
| `<select>` | Formularios | Listas desplegables (seleccion de convocatoria) |
| `<h1>`-`<h3>` | Todas las paginas | Jerarquia de encabezados |

### Jerarquia de plantillas

```
base.html (plantilla padre)
|
|-- extends --> auth/login.html
|-- extends --> auth/register.html
|-- extends --> home.html
|-- extends --> admin/manage_admin.html
|       |-- include --> partials/_user_table.html
|       |-- include --> partials/_user_form_modal.html
|       |-- include --> partials/_user_edit_modal.html
|       +-- include --> partials/_confirm_modal.html
|-- extends --> admin/manage_user.html
|       |-- include --> partials/_user_table.html
|       |-- include --> partials/_user_edit_modal.html
|       +-- include --> partials/_confirm_modal.html
|-- extends --> call/manage_call.html
|       +-- include --> partials/_confirm_modal.html
|-- extends --> call/view_call.html
|-- extends --> project/manage_project.html
|       +-- include --> partials/_confirm_modal.html
+-- extends --> project/view_project.html
        +-- include --> partials/_confirm_modal.html
```

### Componentes reutilizables (partials)

| Partial | Proposito |
|---------|-----------|
| `_confirm_modal.html` | Modal generico de confirmacion antes de eliminar |
| `_user_table.html` | Tabla de usuarios con acciones (editar, eliminar) |
| `_user_form_modal.html` | Modal con formulario para crear usuario |
| `_user_edit_modal.html` | Modal con formulario para editar usuario |

---

## 7. Renderizado Dinamico de Templates

Project Hub usa **Jinja2** como motor de plantillas. Jinja2 se integra con Flask y permite generar HTML de forma dinamica en el servidor antes de enviarlo al navegador.

### 7.1 Herencia de plantillas (`extends` / `block`)

Todas las paginas extienden `base.html` y definen bloques especificos:

```jinja2
{# archivo: home.html #}
{% extends 'base.html' %}

{% block title %}Project HUB - Inicio{% endblock %}

{% block content %}
  <h2>Bienvenido, {{ session.get('user_name') }}</h2>
  {# contenido de la pagina #}
{% endblock %}

{% block scripts %}
  <script src="{{ url_for('static', filename='js/algo.js') }}"></script>
{% endblock %}
```

**Como funciona:** `base.html` define los bloques `title`, `content` y `scripts` como "huecos". Cada pagina hija rellena esos huecos con su contenido especifico. El HTML comun (sidebar, footer, CSS) se hereda automaticamente.

### 7.2 Inclusion de componentes (`include`)

Para reutilizar fragmentos de HTML:

```jinja2
{% include 'partials/_confirm_modal.html' %}
{% include 'partials/_user_table.html' %}
```

**Como funciona:** Jinja2 inserta el contenido del archivo referenciado directamente en el punto de inclusion. Las variables del contexto actual estan disponibles en el partial.

### 7.3 Variables e interpolacion (`{{ }}`)

Las variables que se pasan desde las rutas de Flask se renderizan con dobles llaves:

```python
# En la ruta (Python):
return render_template("home.html", public_projects=projects)
```

```jinja2
{# En el template (HTML): #}
<h2>Bienvenido, {{ session.get('user_name', 'Usuario') }}</h2>
<td>{{ project.name }}</td>
<td>{{ project.created_at.strftime('%d/%m/%Y') }}</td>
```

### 7.4 Condicionales (`{% if %}`)

Permite mostrar u ocultar secciones de HTML segun condiciones:

```jinja2
{# Mostrar menu segun el rol del usuario #}
{% if session.get('role') in ['owner', 'admin'] %}
    <a href="/project/">Proyectos</a>
    <a href="/user/manage_user">Usuarios</a>
{% endif %}

{% if session.get('role') == 'owner' %}
    <a href="/user/manage_admin">Administradores</a>
{% endif %}

{# Mostrar estado activo/inactivo de una convocatoria #}
{% if call.is_active %}
    <span class="badge-active">Activa</span>
{% else %}
    <span class="badge-inactive">Inactiva</span>
{% endif %}
```

### 7.5 Bucles (`{% for %}`)

Para iterar sobre listas y generar filas de tablas, opciones de selects, etc:

```jinja2
{# Generar filas de una tabla de proyectos #}
{% for project in projects %}
<tr>
    <td>{{ project.name }}</td>
    <td>{{ project.description or '---' }}</td>
    <td>{{ project.call.title if project.call else '---' }}</td>
    <td>{{ project.created_at.strftime('%d/%m/%Y') }}</td>
</tr>
{% endfor %}

{# Estado vacio cuando no hay datos #}
{% if not projects %}
    <p class="empty-state">No hay proyectos registrados.</p>
{% endif %}
```

### 7.6 Mensajes flash

Flask permite enviar mensajes temporales entre peticiones. Jinja2 los renderiza en `base.html`:

```python
# En la ruta (Python):
flash("Registro exitoso. Por favor inicia sesion.", "success")
return redirect(url_for("auth.login"))
```

```jinja2
{# En base.html: #}
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="flash-message flash-{{ category }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

**Como funciona:** `flash()` guarda el mensaje en la sesion. En la siguiente peticion, `get_flashed_messages()` lo lee y lo borra de la sesion. Es una comunicacion de un solo uso entre redireccion y renderizado.

### 7.7 Generacion de URLs (`url_for`)

Flask genera URLs de forma segura a partir de nombres de funciones:

```jinja2
{# URL a una ruta #}
<a href="{{ url_for('project.view_project', project_id=project.id) }}">
    Ver Proyecto
</a>

{# URL a un archivo estatico #}
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">

{# URL para formulario #}
<form action="{{ url_for('auth.register') }}" method="POST">
```

**Ventaja:** Si cambias las URLs en las rutas, los templates se actualizan automaticamente sin editar HTML.

### 7.8 Variables con `set`

Para configurar componentes reutilizables con datos especificos:

```jinja2
{# En manage_admin.html #}
{% set users = admins %}
{% set update_endpoint = 'user.update_admin' %}
{% set delete_endpoint = 'user.delete_admin' %}
{% include 'partials/_user_table.html' %}
```

Esto permite que `_user_table.html` sea generico y funcione tanto para admins como para leaders.

### 7.9 Flujo completo de renderizado

```
1. El usuario hace GET /project/5

2. Flask busca la ruta que coincide:
   @project_bp.route("/<int:project_id>", methods=["GET"])
   def view_project(project_id):

3. La ruta consulta la base de datos:
   project = ProjectService.get_by_id(project_id)

4. Flask llama a Jinja2 con el template y las variables:
   return render_template("project/view_project.html", project=project)

5. Jinja2 procesa el template:
   a. Carga "project/view_project.html"
   b. Ve que extiende "base.html" -> carga base.html
   c. Reemplaza los bloques (title, content, scripts)
   d. Evalua condicionales ({% if session.role == 'admin' %})
   e. Itera sobre listas ({% for d in project.deliverables %})
   f. Interpola variables ({{ project.name }})
   g. Incluye partials ({% include '_confirm_modal.html' %})

6. Jinja2 retorna una cadena HTML completa

7. Flask la envia como respuesta HTTP al navegador
```

---

## 8. Sistema de Autorizacion

### Decoradores de acceso (`utils/decorators.py`)

| Decorador | Quien puede acceder | Si no cumple |
|-----------|---------------------|-------------|
| `@login_required` | Cualquier usuario autenticado | Redirige a `/auth/login` |
| `@admin_required` | Usuarios con rol `admin` u `owner` | Redirige a `/home` |
| `@owner_required` | Solo usuarios con rol `owner` | Redirige a `/home` |

### Verificacion de convocatoria activa

Los leaders solo pueden crear/editar/eliminar proyectos y archivos si la convocatoria asociada esta activa (`opening_date <= ahora <= closing_date`). Los admin y owner pueden modificar independientemente del estado de la convocatoria.

### Verificacion de propiedad de proyecto

Para operaciones sobre proyectos y archivos, se verifica que:
- El usuario sea admin/owner (acceso completo), O
- El usuario sea el leader asignado al proyecto

### Visibilidad

Un archivo es visible para usuarios externos (no admin, no owner, no leader del proyecto) solo si **ambas** condiciones se cumplen:
1. El proyecto es publico (`project.is_public == True`)
2. El archivo es publico (`deliverable.is_public == True`)
