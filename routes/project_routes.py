from flask import Blueprint, render_template, request, jsonify, session
from services.project_service import ProjectService
from services.call_service import CallService
from utils.decorators import login_required


def _check_call_active(project_id=None, call_id=None):
    """Return error response if call is inactive and user is not admin/owner."""
    role = session.get("role")
    if role in ["admin", "owner"]:
        return None

    if project_id:
        project = ProjectService.get_by_id(project_id)
        if project and project.call and not project.call.is_active:
            return jsonify({"error": "La convocatoria no está activa. No se pueden realizar cambios."}), 403
    elif call_id:
        call = CallService.get_by_id(call_id)
        if not call or not call.is_active:
            return jsonify({"error": "La convocatoria no está activa. No se pueden realizar cambios."}), 403
    return None

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

        if not call_id:
            errors["call_id"] = "La convocatoria es obligatoria."

        if errors:
            return jsonify({"errors": errors}), 422

        blocked = _check_call_active(call_id=call_id)
        if blocked:
            return blocked

        is_public = data.get("is_public", False) if data else False

        project, error, status_code = ProjectService.create(
            name=name,
            description=description,
            leader_id=session.get("user_id"),
            call_id=call_id,
            is_public=bool(is_public),
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
    user_id = session.get("user_id")
    role = session.get("role")
    projects = ProjectService.get_all(user_id, role)
    calls = CallService.get_all()

    if role not in ["admin", "owner"]:
        user_project_call_ids = [p.call_id for p in projects if p.call_id]
        calls = [c for c in calls if c.id not in user_project_call_ids and c.is_active]

    return render_template(
        "project/manage_project.html", projects=projects, calls=calls
    )


@project_bp.route("/<int:project_id>", methods=["PUT"])
@login_required
def update_project(project_id):
    try:
        blocked = _check_call_active(project_id=project_id)
        if blocked:
            return blocked

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

        is_public = data.get("is_public", False) if data else False

        project, error, status_code = ProjectService.update(
            project_id=project_id,
            user_id=session.get("user_id"),
            role=session.get("role"),
            name=name,
            description=description,
            is_public=bool(is_public),
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


@project_bp.route("/<int:project_id>/visibility", methods=["PATCH"])
@login_required
def toggle_visibility(project_id):
    try:
        blocked = _check_call_active(project_id=project_id)
        if blocked:
            return blocked

        project, error, status_code = ProjectService.toggle_visibility(
            project_id=project_id,
            user_id=session.get("user_id"),
            role=session.get("role"),
        )

        if error:
            return jsonify({"error": error}), status_code

        return jsonify({
            "message": "Visibilidad actualizada.",
            "is_public": project.is_public,
        }), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


@project_bp.route("/<int:project_id>", methods=["DELETE"])
@login_required
def delete_project(project_id):
    try:
        blocked = _check_call_active(project_id=project_id)
        if blocked:
            return blocked

        project, error, status_code = ProjectService.delete(
            project_id=project_id,
            user_id=session.get("user_id"),
            role=session.get("role"),
        )

        if error:
            return jsonify({"error": error}), status_code

        return jsonify({"message": "Proyecto eliminado exitosamente."})

    except Exception as e:
        return jsonify({"error": "Error interno del servidor."}), 500


@project_bp.route("/<int:project_id>", methods=["GET"])
@login_required
def view_project(project_id):
    project = ProjectService.get_by_id(project_id)
    if not project:
        return render_template("404.html"), 404

    role = session.get("role")
    user_id = session.get("user_id")

    # Permission check: allow if admin/owner, leader, or project is public
    if role not in ["admin", "owner"] and project.leader_id != user_id and not project.is_public:
        return render_template("403.html"), 403

    return render_template("project/view_project.html", project=project)
