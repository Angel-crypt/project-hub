# Services

Capa de logica de negocio. Cada servicio encapsula las operaciones de un modelo y es llamado desde las rutas. Ningun servicio accede directamente a `request` o `session` de Flask. Todas las funciones tienen type hints explicitos en parametros y retorno.

## Archivos

| Archivo | Modelo | Que hace |
|---------|--------|----------|
| `auth_service.py` | User | Registro y login con validacion de credenciales |
| `user_service.py` | User | CRUD completo de usuarios (admins y leaders) |
| `call_service.py` | Call | CRUD de convocatorias con validacion de fechas y unicidad de titulo |
| `project_service.py` | Project | CRUD de proyectos con control de permisos y visibilidad |
| `deliverable_service.py` | Deliverable | Subida de archivos con validacion de tipo, firma y tamano |

## Patron de retorno

Los metodos que modifican datos retornan una tupla tipada:

```python
tuple[Optional[Entidad], Optional[str], Optional[int]]
```

- **Exito**: `(entidad, None, None)` o `(entidad, None, 201)`
- **Error**: `(None, "mensaje de error", codigo_http)`

Ejemplo de uso desde una ruta:

```python
project, error, status_code = ProjectService.create(name=name, ...)
if error:
    return jsonify({"error": error}), status_code
```

## Detalle por servicio

### AuthService (`auth_service.py`)

| Metodo | Firma |
|--------|-------|
| `register` | `(enrollment_number: str, name: str, password: str) -> tuple[Optional[User], Optional[str], Optional[int]]` |
| `login` | `(enrollment_number: str, password: str) -> tuple[Optional[User], Optional[str], Optional[int]]` |

- `register`: crea usuario con rol LEADER. Valida matricula (max 10), nombre y contrasena (min 6). Verifica duplicados.
- `login`: busca usuario por matricula y verifica contrasena con hash.

### UserService (`user_service.py`)

| Metodo | Firma |
|--------|-------|
| `create` | `(enrollment_number: str, name: str, password: str, role: str = "leader") -> tuple[Optional[User], Optional[str], Optional[int]]` |
| `get_admins` | `() -> list[User]` |
| `get_leaders` | `() -> list[User]` |
| `get_by_id` | `(user_id: int) -> Optional[User]` |
| `get_by_enrollment` | `(enrollment_number: str) -> Optional[User]` |
| `update` | `(user_id: int, name: Optional[str], password: Optional[str], role: Optional[RoleEnum]) -> tuple[Optional[User], Optional[str], Optional[int]]` |
| `delete` | `(user_id: int) -> tuple[Optional[User], Optional[str], Optional[int]]` |

### CallService (`call_service.py`)

Funcion auxiliar: `_parse_date(value: Union[str, datetime, None]) -> Optional[datetime]`

| Metodo | Firma |
|--------|-------|
| `create` | `(title: str, description: str, opening_date: Union[str, datetime], closing_date: Union[str, datetime]) -> tuple[Optional[Call], Optional[str], Optional[int]]` |
| `get_all` | `() -> list[Call]` |
| `get_by_id` | `(call_id: int) -> Optional[Call]` |
| `update` | `(call_id: int, title: Optional[str], description: Optional[str], opening_date: Optional[Union[str, datetime]], closing_date: Optional[Union[str, datetime]]) -> tuple[Optional[Call], Optional[str], Optional[int]]` |
| `delete` | `(call_id: int) -> tuple[Optional[Call], Optional[str], Optional[int]]` |

- `create`: valida titulo unico y fecha de cierre posterior a apertura.
- `delete`: no permite eliminar si tiene proyectos asociados (409).
- Las fechas aceptan `str` formato `"YYYY-MM-DD"` o `datetime`.

### ProjectService (`project_service.py`)

| Metodo | Firma |
|--------|-------|
| `create` | `(name: str, description: str, leader_id: int, call_id: int, is_public: bool = False) -> tuple[Optional[Project], Optional[str], Optional[int]]` |
| `get_all` | `(user_id: int, role: str) -> list[Project]` |
| `get_by_id` | `(project_id: int) -> Optional[Project]` |
| `get_public` | `() -> list[Project]` |
| `update` | `(project_id: int, user_id: int, role: str, name: Optional[str], description: Optional[str], is_public: Optional[bool]) -> tuple[Optional[Project], Optional[str], Optional[int]]` |
| `toggle_visibility` | `(project_id: int, user_id: int, role: str) -> tuple[Optional[Project], Optional[str], Optional[int]]` |
| `delete` | `(project_id: int, user_id: int, role: str) -> tuple[Optional[Project], Optional[str], Optional[int]]` |

- `create`: valida nombre unico y limite de un proyecto por leader por convocatoria.
- `get_all`: admin/owner ven todos, leaders solo los propios.
- `update`: solo el leader puede editar (admin/owner no).

### DeliverableService (`deliverable_service.py`)

| Metodo | Firma |
|--------|-------|
| `allowed_file` | `(filename: str) -> bool` |
| `validate_file_content` | `(file: FileStorage) -> bool` |
| `create` | `(name: str, description: str, project_id: int, file: FileStorage, is_public: bool = False) -> tuple[Optional[Deliverable], Optional[str], Optional[int]]` |
| `toggle_visibility` | `(deliverable_id: int, user_id: int, role: str) -> tuple[Optional[Deliverable], Optional[str], Optional[int]]` |
| `get_by_project` | `(project_id: int) -> list[Deliverable]` |

- `create`: valida extension, firma binaria y tamano (max 10MB). Genera nombre unico con UUID.
- `file` es de tipo `werkzeug.datastructures.FileStorage` (el objeto que Flask recibe de `request.files`).

## Validacion de archivos

El servicio de deliverables valida archivos en dos niveles:

1. **Extension**: solo se permiten `pdf`, `png`, `jpg`, `jpeg`, `doc`, `docx`
2. **Firma binaria (magic bytes)**: verifica que el contenido real del archivo coincida con su extension

| Extension | Firma esperada |
|-----------|---------------|
| pdf | `%PDF` |
| png | `\x89PNG\r\n\x1a\n` |
| jpg/jpeg | `\xff\xd8\xff` |
| doc | `\xd0\xcf\x11\xe0` |
| docx | `PK\x03\x04` |
