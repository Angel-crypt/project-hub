# Routes

Controladores de la aplicacion organizados como **Flask Blueprints**. Cada archivo maneja las rutas de un modulo especifico. Todas las funciones tienen type hints en parametros y retorno, y un comentario descriptivo antes de cada ruta.

## Archivos

| Archivo | Prefijo | Que hace |
|---------|---------|----------|
| `auth_routes.py` | `/auth` | Registro, login y logout |
| `user_routes.py` | `/user` | CRUD de administradores y lideres |
| `call_routes.py` | `/call` | CRUD de convocatorias |
| `project_routes.py` | `/project` | CRUD de proyectos |
| `deliverable_routes.py` | `/deliverable` | Subida, descarga y gestion de archivos |

## Tipos de retorno

Las funciones usan tipos explicitos de `werkzeug.wrappers.Response`:

| Tipo de retorno | Cuando se usa |
|-----------------|---------------|
| `-> str` | Rutas GET que renderizan HTML con `render_template()` |
| `-> Response` | Rutas que retornan JSON (`jsonify()`), redirects o archivos |
| `-> str \| Response` | Rutas GET/POST que pueden retornar HTML o redirect segun el metodo |

## Funciones auxiliares

| Funcion | Archivo | Firma |
|---------|---------|-------|
| `_check_call_active` | `project_routes.py` | `(project_id: Optional[int], call_id: Optional[int]) -> Optional[tuple[Response, int]]` |

Retorna error 403 si la convocatoria esta inactiva y el usuario no es admin/owner. Retorna `None` si todo esta bien.

## Endpoints

### Autenticacion (`/auth`)

| Metodo | Ruta | Funcion | Retorno | Acceso |
|--------|------|---------|---------|--------|
| GET | `/auth/register` | `register() -> str \| Response` | HTML | Publico |
| POST | `/auth/register` | `register() -> str \| Response` | Redirect | Publico |
| GET | `/auth/login` | `login() -> str \| Response` | HTML | Publico |
| POST | `/auth/login` | `login() -> str \| Response` | Redirect | Publico |
| GET | `/auth/logout` | `logout() -> Response` | Redirect | Publico |

### Usuarios (`/user`)

| Metodo | Ruta | Funcion | Retorno | Acceso |
|--------|------|---------|---------|--------|
| GET | `/user/manage_admin` | `manage_admin() -> str \| Response` | HTML | owner |
| POST | `/user/manage_admin` | `manage_admin() -> str \| Response` | Redirect | owner |
| PUT | `/user/admin/<id>` | `update_admin(user_id: int) -> Response` | JSON | owner |
| DELETE | `/user/admin/<id>` | `delete_admin(user_id: int) -> Response` | JSON | owner |
| GET | `/user/manage_user` | `manage_user() -> str` | HTML | admin/owner |
| PUT | `/user/leader/<id>` | `update_leader(user_id: int) -> Response` | JSON | admin/owner |
| DELETE | `/user/leader/<id>` | `delete_leader(user_id: int) -> Response` | JSON | admin/owner |

### Convocatorias (`/call`)

| Metodo | Ruta | Funcion | Retorno | Acceso |
|--------|------|---------|---------|--------|
| GET | `/call/` | `view_all() -> str` | HTML | login |
| POST | `/call/` | `create_call() -> Response` | JSON 201 | admin/owner |
| GET | `/call/<id>` | `view_call(call_id: int) -> str` | HTML | login |
| PUT | `/call/<id>` | `update_call(call_id: int) -> Response` | JSON | admin/owner |
| DELETE | `/call/<id>` | `delete_call(call_id: int) -> Response` | JSON | admin/owner |

### Proyectos (`/project`)

| Metodo | Ruta | Funcion | Retorno | Acceso |
|--------|------|---------|---------|--------|
| GET | `/project/` | `view_all() -> str` | HTML | login |
| POST | `/project/` | `create_project() -> Response` | JSON 201 | login |
| GET | `/project/<id>` | `view_project(project_id: int) -> str` | HTML | login (*) |
| PUT | `/project/<id>` | `update_project(project_id: int) -> Response` | JSON | login (*) |
| PATCH | `/project/<id>/visibility` | `toggle_visibility(project_id: int) -> Response` | JSON | login (*) |
| DELETE | `/project/<id>` | `delete_project(project_id: int) -> Response` | JSON | login (*) |

### Archivos (`/deliverable`)

| Metodo | Ruta | Funcion | Retorno | Acceso |
|--------|------|---------|---------|--------|
| GET | `/deliverable/view/<id>` | `view_deliverable(deliverable_id: int) -> Response` | Archivo | login (*) |
| GET | `/deliverable/download/<id>` | `download_deliverable(deliverable_id: int) -> Response` | Archivo | login (*) |
| POST | `/deliverable/upload/<project_id>` | `upload_deliverable(project_id: int) -> Response` | JSON 201 | leader del proyecto |
| PUT | `/deliverable/<id>` | `update_deliverable(deliverable_id: int) -> Response` | JSON | leader del proyecto |
| PATCH | `/deliverable/<id>/visibility` | `toggle_file_visibility(deliverable_id: int) -> Response` | JSON | leader/admin/owner |
| DELETE | `/deliverable/<id>` | `delete_deliverable(deliverable_id: int) -> Response` | JSON | leader/admin/owner |

> (*) Los proyectos/archivos publicos son accesibles para cualquier usuario autenticado. Los privados solo para el leader, admin u owner. Las operaciones de escritura requieren convocatoria activa (excepto admin/owner).

## Patron de respuestas

- **Rutas GET de paginas**: retornan `str` (HTML) con `render_template()`
- **Rutas POST/PUT/PATCH/DELETE de datos**: retornan `Response` (JSON) con `jsonify()`
- **Errores de validacion**: JSON con codigo `422`
- **Errores de autorizacion**: JSON con codigo `403`
- **Recurso no encontrado**: JSON con codigo `404`
