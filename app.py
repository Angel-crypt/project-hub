from flask import Flask
from models import db
from routes.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)

    # Configuración
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projecthub.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "WyRYSTp3W3ca8uPw"

    # Inicializar db con la app
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp)

    # IMPORTANTE: Retornar la app
    return app
