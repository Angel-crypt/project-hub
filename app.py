from flask import Flask, redirect, url_for, render_template
from models import db
from routes import auth_bp, user_bp, call_bp
from utils.decorators import login_required
from utils.seed import seed_users, seed_calls, seed_projects


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projecthub.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "WyRYSTp3W3ca8uPw"

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(call_bp)

    with app.app_context():
        db.create_all()
        seed_users()
        seed_calls()
        seed_projects()

    @app.route("/")
    def index():
        return redirect(url_for("home"))

    @app.route("/home")
    @login_required
    def home():
        return render_template("home.html")

    return app
