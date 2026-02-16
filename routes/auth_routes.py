from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.wrappers import Response
from services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# GET: muestra formulario | POST: procesa registro y redirige a login
@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> str | Response:
    if request.method == "POST":
        user, error, status_code = AuthService.register(
            enrollment_number=request.form.get("enrollment_number"),
            name=request.form.get("name"),
            password=request.form.get("password"),
        )

        if error:
            return (
                render_template(
                    "auth/register.html", error=error, status_code=status_code
                ),
                status_code,
            )

        flash("Registro exitoso. Por favor inicia sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# GET: muestra formulario | POST: valida credenciales y crea sesion
@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if request.method == "POST":
        user, error, status_code = AuthService.login(
            enrollment_number=request.form.get("enrollment_number"),
            password=request.form.get("password"),
        )

        if error:
            return (
                render_template(
                    "auth/login.html", error=error, status_code=status_code
                ),
                status_code,
            )

        session["user_id"] = user.id
        session["user_name"] = user.name
        session["role"] = user.role.value
        return redirect(url_for("home"))

    return render_template("auth/login.html")


# Limpia la sesion y redirige a login
@auth_bp.route("/logout")
def logout() -> Response:
    session.clear()
    return redirect(url_for("auth.login"))
