# Utils

Funciones auxiliares usadas en toda la aplicacion.

## Archivos

| Archivo | Que hace |
|---------|----------|
| `decorators.py` | Decoradores para proteger rutas segun autenticacion y rol |
| `seed.py` | Datos iniciales que se cargan al crear la base de datos |

## Decoradores (`decorators.py`)

Se aplican a las rutas con `@decorador` para restringir el acceso. Cada decorador recibe una funcion y retorna una funcion decorada:

| Decorador | Quien puede acceder | Si no cumple |
|-----------|---------------------|--------------|
| `@login_required` | Cualquier usuario con sesion activa | Redirige a `/auth/login` |
| `@admin_required` | Usuarios con rol `admin` u `owner` | Redirige a `/home` |
| `@owner_required` | Solo usuarios con rol `owner` | Redirige a `/home` |

Ejemplo de uso con las firmas tipadas de las rutas:

```python
@call_bp.route("/", methods=["POST"])
@admin_required
def create_call() -> Response:
    ...

@call_bp.route("/<int:call_id>", methods=["GET"])
@login_required
def view_call(call_id: int) -> str:
    ...
```

Los decoradores verifican la sesion de Flask (`session["user_id"]` y `session["role"]`). `@admin_required` y `@owner_required` ya incluyen la verificacion de login, no es necesario combinarlos con `@login_required`.

## Seed (`seed.py`)

Carga datos de prueba al iniciar la aplicacion si no existen. Se ejecuta automaticamente desde `app.py` dentro de `create_app()`.

### Usuarios por defecto

| Matricula | Nombre | Contrasena | Rol |
|-----------|--------|------------|-----|
| `OWNER001` | Owner | `owner123` | owner |
| `ADMIN001` | Admin | `admin123` | admin |
| `LEADER001` | Leader | `leader123` | leader |

### Convocatorias por defecto

| Titulo | Apertura | Cierre |
|--------|----------|--------|
| Convocatoria de Proyectos 2026 | 2026-01-01 | 2026-02-28 |
| Becas de Investigacion Q1 2026 | 2026-01-15 | 2026-03-15 |
| Hackathon Universitario 2026 | 2026-02-01 | 2026-02-15 |

### Proyectos por defecto

Se crean 2 proyectos asignados al primer leader encontrado:

| Nombre | Convocatoria | Publico |
|--------|-------------|---------|
| Proyecto de Energia Renovable | #1 | Si |
| Aplicacion de Salud Mental | #2 | No |

Las funciones `seed_users()`, `seed_calls()` y `seed_projects()` verifican si el dato ya existe antes de insertarlo, asi que correr la app multiples veces no genera duplicados.
