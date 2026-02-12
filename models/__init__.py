from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User, RoleEnum

__all__ = ["db", "User", "RoleEnum"]
