from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        enrrollment_number = request.form.get("enrrollment_number")
        name = request.form.get("name")
        password = request.form.get("password")
        role = request.form.get("role", "leader")

        response, status_code = AuthService.register(
            enrrollment_number, name, password, role
        )

        if status_code == 201:
            flash("Registro exitoso. Por favor inicia sesión.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash(response["message"], "error")
            return render_template("auth/register.html"), status_code

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        enrrollment_number = request.form.get("name")
        password = request.form.get("password")

        response, status_code = AuthService.login(enrrollment_number, password)

        if status_code == 200:
            user = response["user"]
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["role"] = user.role.value
            return redirect(url_for("dashboard.dashboard_index"))
        else:
            return (
                render_template("auth/login.html", error=response["message"], status_code=status_code),
                status_code,
            )

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
