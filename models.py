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

class AuthUser(UserMixin):
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
                password_hash = generate_password_hash(password)
                cursor = conn.execute(
                    "INSERT INTO auth_users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, password_hash)
                )
                conn.commit()
                return {'success': True, 'id': cursor.lastrowid}
        except sqlite3.IntegrityError as e:
            error_msg = 'El usuario ya existe' if 'username' in str(e) else 'El email ya existe'
            return {'success': False, 'error': error_msg}
        except Exception:
            return {'success': False, 'error': 'Error al crear usuario'}
    
    @staticmethod
    def get_user_object(user_id):
        """Retorna objeto AuthUser para Flask-Login"""
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
        """Verifica credenciales de usuario"""
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
