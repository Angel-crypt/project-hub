from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.user_service import UserService
from utils.decorators import admin_required, owner_required

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/manage_admin", methods=["GET", "POST"])
@owner_required
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


@user_bp.route("/manage_user", methods=["GET"])
@admin_required
def manage_user():
    leaders = UserService.get_leaders()
    return render_template("admin/manage_user.html", leaders=leaders)


@user_bp.route("/admin/<int:user_id>", methods=["PUT"])
@owner_required
def update_admin(user_id):
    data = request.get_json()
    name = data.get("name", "").strip() if data else ""

    if not name:
        return jsonify({"error": "El nombre es obligatorio."}), 422

    user, error, status_code = UserService.update(user_id, name=name)
    if error:
        return jsonify({"error": error}), status_code

    return jsonify({"message": "Administrador actualizado."})


@user_bp.route("/admin/<int:user_id>", methods=["DELETE"])
@owner_required
def delete_admin(user_id):
    user, error, status_code = UserService.delete(user_id)
    if error:
        return jsonify({"error": error}), status_code

    return jsonify({"message": "Administrador eliminado."})


@user_bp.route("/leader/<int:user_id>", methods=["PUT"])
@admin_required
def update_leader(user_id):
    data = request.get_json()
    name = data.get("name", "").strip() if data else ""

    if not name:
        return jsonify({"error": "El nombre es obligatorio."}), 422

    user, error, status_code = UserService.update(user_id, name=name)
    if error:
        return jsonify({"error": error}), status_code

    return jsonify({"message": "Usuario actualizado."})


@user_bp.route("/leader/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_leader(user_id):
    user, error, status_code = UserService.delete(user_id)
    if error:
        return jsonify({"error": error}), status_code

    return jsonify({"message": "Usuario eliminado."})
