from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.user_service import UserService
from utils.decorators import admin_required

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/manage_admin", methods=["GET", "POST"])
@admin_required
def manage_admin():
    if request.method == "POST":
        user, error, status_code = UserService.create(
            enrrollment_number=request.form.get("enrrollment_number"),
            name=request.form.get("name"),
            password=request.form.get("password"),
            role="admin",
        )

        if error:
            admins = UserService.get_admins()
            return (
                render_template(
                    "admin/manage_admin.html", admins=admins, error=error, status_code=status_code
                ),
                status_code,
            )

        flash("Administrador registrado exitosamente.", "success")
        return redirect(url_for("user.manage_admin"))

    admins = UserService.get_admins()
    return render_template("admin/manage_admin.html", admins=admins)