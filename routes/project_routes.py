from flask import Blueprint, render_template, request, jsonify
from services.project_service import ProjectService
from utils.decorators import login_required, admin_required
from datetime import datetime

project_bp = Blueprint("project", __name__, url_prefix="/project")


@project_bp.route("/", methods=["POST"])
@login_required
def create_project():
    try:
        data = request.get_json()

        name = data.get("name", "").strip() if data else ""
        description = data.get("description", "").strip() if data else ""
        call_id = data.get("call_id") if data else None

        errors = {}

        if not name:
            errors["name"] = "El nombre es obligatorio."
        elif len(name) > 80:
            errors["name"] = "El nombre no puede exceder 80 caracteres."

        if errors:
            return jsonify({"errors": errors}), 422

        project, error, status_code = ProjectService.create(
            name=name,
            description=description,
            leader_id=request.session.get("user_id"),
            call_id=call_id,
        )

        if error:
            return jsonify({"error": error}), status_code

        return (
            jsonify(
                {
                    "message": "Proyecto registrado exitosamente.",
                    "project_id": project.id,
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


@project_bp.route("/", methods=["GET"])
@login_required
def view_all():
    user_id = request.session.get("user_id")
    role = request.session.get("role")
    projects = ProjectService.get_all(user_id, role)
    return render_template("project/manage_project.html", projects=projects)


@project_bp.route("/<int:project_id>", methods=["PUT"])
@login_required
def update_project(project_id):
    try:
        data = request.get_json()

        name = data.get("name", "").strip() if data else ""
        description = data.get("description", "").strip() if data else ""

        errors = {}

        if not name:
            errors["name"] = "El nombre es obligatorio."
        elif len(name) > 80:
            errors["name"] = "El nombre no puede exceder 80 caracteres."

        if errors:
            return jsonify({"errors": errors}), 422

        project, error, status_code = ProjectService.update(
            project_id=project_id,
            user_id=request.session.get("user_id"),
            role=request.session.get("role"),
            name=name,
            description=description
        )

        if error:
            return jsonify({"error": error}), status_code

        return (
            jsonify(
                {
                    "message": "Proyecto actualizado exitosamente.",
                    "project_id": project.id,
                }
            ),
            200,
        )

    except Exception as e:
        print(f"Error in update_project: {e}")
        return jsonify({"error": "Error interno del servidor."}), 500


@project_bp.route("/<int:project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id):
    try:
        project, error, status_code = ProjectService.delete(
            project_id=project_id,
            user_id=request.session.get("user_id"),
            role=request.session.get("role")
        )

        if error:
            return jsonify({"error": error}), status_code

        return jsonify({"message": "Proyecto eliminado exitosamente."})

    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500
