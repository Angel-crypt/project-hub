from flask import Flask, redirect, url_for, render_template
from models import db
from routes import auth_bp
from utils.decorators import login_required


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

    @app.route("/")
    def index():
        return redirect(url_for("home"))

    @app.route("/home")
    @login_required
    def home():
        return render_template("home.html")

    return app
