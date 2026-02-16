from .auth_routes import auth_bp
from .user_routes import user_bp
from .call_routes import call_bp
from .project_routes import project_bp
from .deliverable_routes import deliverable_bp

__all__ = ["auth_bp", "user_bp", "call_bp", "project_bp", "deliverable_bp"]
