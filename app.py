from flask import Flask, session, redirect, url_for
from models import db
from routes import auth_bp


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

    # Simple home route
    @app.route("/home")
    def home():
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f"<h1>Bienvenido {session.get('user_name', 'Usuario')}</h1><a href='{url_for('auth.logout')}'>Cerrar Sesión</a>"

    @app.route("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("home"))
        return redirect(url_for("auth.login"))

    return app
