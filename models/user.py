from models import db
from datetime import datetime
import enum


class RoleEnum(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    LEADER = "leader"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    enrollment_number = db.Column(db.String(10), unique=True, nullable=False, index=True)
    name = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.LEADER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, enrollment_number, name, password, role=RoleEnum.LEADER):
        self.enrollment_number = enrollment_number
        self.name = name
        self.set_password(password)
        self.role = role
    
    def __repr__(self):
        return f"<Usuario {self.name}>"

    def set_password(self, password):
        from werkzeug.security import generate_password_hash

        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash

        return check_password_hash(self.password_hash, password)
