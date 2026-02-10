import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

DATABASE = 'database.db'

def get_db():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa las tablas de la base de datos"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS auth_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                is_public BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES auth_users(id) ON DELETE CASCADE
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_projects_user_id ON projects(user_id)
        """)
        
        conn.commit()

class User(UserMixin):
    """Modelo para usuarios"""
    
    def __init__(self, id, username, email, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.created_at = created_at
    
    @staticmethod
    def create(username, email, password):
        """Crea un nuevo usuario"""
        try:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO auth_users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password))
                )
                conn.commit()
                return {'success': True}
        except sqlite3.IntegrityError:
            return {'success': False, 'error': 'El usuario o email ya existe'}
        except Exception:
            return {'success': False, 'error': 'Error al crear usuario'}
    
    @staticmethod
    def get_user_object(user_id):
        """Obtiene un usuario por ID"""
        try:
            with get_db() as conn:
                user = conn.execute(
                    "SELECT id, username, email, created_at FROM auth_users WHERE id = ?",
                    (user_id,)
                ).fetchone()
                
                if user:
                    return AuthUser(user['id'], user['username'], user['email'], user['created_at'])
                return None
        except Exception:
            return None
    
    @staticmethod
    def verify_password(username, password):
        """Verifica las credenciales del usuario"""
        try:
            with get_db() as conn:
                user = conn.execute(
                    "SELECT id, username, email, password_hash, created_at FROM auth_users WHERE username = ?",
                    (username,)
                ).fetchone()
                
                if user and check_password_hash(user['password_hash'], password):
                    return {'success': True, 'user': AuthUser(user['id'], user['username'], user['email'], user['created_at'])}
                return {'success': False, 'error': 'Credenciales inválidas'}
        except Exception:
            return {'success': False, 'error': 'Error al verificar credenciales'}

class Project:
    """
    Modelo para proyectos
    """
    
    def __init__(self, id, user_id, title, description, is_public, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.is_public = is_public
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """Convierte el proyecto a diccionario para respuestas JSON"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'is_public': self.is_public,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    
    def can_view(self, requesting_user_id=None):
        if self.is_public:
            return True
        return requesting_user_id is not None and self.user_id == requesting_user_id
    
    def can_edit(self, requesting_user_id):
        return requesting_user_id is not None and self.user_id == requesting_user_id
    
    def can_delete(self, requesting_user_id):
        return requesting_user_id is not None and self.user_id == requesting_user_id
    
    @staticmethod
    def _from_row(row):
        """Construye un objeto Project desde una fila de la BD"""
        return Project(
            row['id'], row['user_id'], row['title'], row['description'],
            row['is_public'], row['created_at'], row['updated_at']
        )
    
    @staticmethod
    def create(user_id, title, description=None, is_public=False):
        """Crea un nuevo proyecto"""
        try:
            with get_db() as conn:
                cursor = conn.execute(
                    "INSERT INTO projects (user_id, title, description, is_public) VALUES (?, ?, ?, ?)",
                    (user_id, title, description, is_public)
                )
                conn.commit()
                return {'success': True, 'id': cursor.lastrowid}
        except sqlite3.IntegrityError:
            return {'success': False, 'error': 'Error de integridad al crear proyecto'}
        except Exception:
            return {'success': False, 'error': 'Error al crear proyecto'}
    
    @staticmethod
    def get_by_id(project_id, requesting_user_id=None):
        """
        Obtiene un proyecto por ID con control de acceso
        """
        try:
            with get_db() as conn:
                row = conn.execute(
                    "SELECT id, user_id, title, description, is_public, created_at, updated_at FROM projects WHERE id = ?",
                    (project_id,)
                ).fetchone()
                
                if not row:
                    return {'success': False, 'error': 'Proyecto no encontrado'}
                
                project = Project._from_row(row)
                
                if not project.can_view(requesting_user_id):
                    return {'success': False, 'error': 'No tienes permisos para acceder a este proyecto'}
                
                return {'success': True, 'data': project}
                
        except sqlite3.Error:
            return {'success': False, 'error': 'Error de base de datos'}
        except Exception:
            return {'success': False, 'error': 'Error interno'}
    
    @staticmethod
    def get_user_projects(user_id):
        """
        Obtiene todos los proyectos de un usuario
        """
        try:
            with get_db() as conn:
                rows = conn.execute(
                    "SELECT id, user_id, title, description, is_public, created_at, updated_at FROM projects WHERE user_id = ? ORDER BY created_at DESC",
                    (user_id,)
                ).fetchall()
                
                return {'success': True, 'data': [Project._from_row(row) for row in rows]}
                
        except sqlite3.Error:
            return {'success': False, 'error': 'Error de base de datos'}
        except Exception:
            return {'success': False, 'error': 'Error interno'}
    
    @staticmethod
    def get_public_projects(exclude_user_id=None):
        """
        Obtiene todos los proyectos públicos
        """
        try:
            with get_db() as conn:
                if exclude_user_id:
                    rows = conn.execute(
                        "SELECT id, user_id, title, description, is_public, created_at, updated_at FROM projects WHERE is_public = 1 AND user_id != ? ORDER BY created_at DESC",
                        (exclude_user_id,)
                    ).fetchall()
                else:
                    rows = conn.execute(
                        "SELECT id, user_id, title, description, is_public, created_at, updated_at FROM projects WHERE is_public = 1 ORDER BY created_at DESC"
                    ).fetchall()
                
                return {'success': True, 'data': [Project._from_row(row) for row in rows]}
                
        except sqlite3.Error:
            return {'success': False, 'error': 'Error de base de datos'}
        except Exception:
            return {'success': False, 'error': 'Error interno'}
    
    @staticmethod
    def update(project_id, user_id, title, description, is_public):
        """
        Actualiza un proyecto
        """
        try:
            with get_db() as conn:
                row = conn.execute(
                    "SELECT id, user_id, title, description, is_public, created_at, updated_at FROM projects WHERE id = ?",
                    (project_id,)
                ).fetchone()
                
                if not row:
                    return {'success': False, 'error': 'Proyecto no encontrado'}
                
                project = Project._from_row(row)
                
                if not project.can_edit(user_id):
                    return {'success': False, 'error': 'No tienes permisos para editar este proyecto'}
                
                conn.execute(
                    "UPDATE projects SET title = ?, description = ?, is_public = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (title, description, is_public, project_id)
                )
                conn.commit()
                return {'success': True}
                
        except Exception:
            return {'success': False, 'error': 'Error al actualizar proyecto'}
    
    @staticmethod
    def delete(project_id, user_id):
        """
        Elimina un proyecto
        """
        try:
            with get_db() as conn:
                row = conn.execute(
                    "SELECT id, user_id, title, description, is_public, created_at, updated_at FROM projects WHERE id = ?",
                    (project_id,)
                ).fetchone()
                
                if not row:
                    return {'success': False, 'error': 'Proyecto no encontrado'}
                
                project = Project._from_row(row)
                
                if not project.can_delete(user_id):
                    return {'success': False, 'error': 'No tienes permisos para eliminar este proyecto'}
                
                conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
                conn.commit()
                return {'success': True}
                
        except Exception:
            return {'success': False, 'error': 'Error al eliminar proyecto'}
