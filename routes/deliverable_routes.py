from flask import Blueprint, request, jsonify, session, current_app, send_from_directory
from werkzeug.wrappers import Response
from services.deliverable_service import DeliverableService
from models.project import Project
from models.deliverable import Deliverable
from models import db
from utils.decorators import login_required
import os

_CALL_INACTIVE_MSG = "La convocatoria no está activa. No se pueden realizar cambios."

deliverable_bp = Blueprint("deliverable", __name__, url_prefix="/deliverable")


# Muestra el archivo en el navegador (inline). Verifica permisos de visibilidad
@deliverable_bp.route("/view/<int:deliverable_id>", methods=["GET"])
@login_required
def view_deliverable(deliverable_id: int) -> Response:
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    project = deliverable.project

    role = session.get("role")
    user_id = session.get("user_id")

    # Acceso: admin/owner, leader del proyecto, o si ambos (proyecto y archivo) son publicos
    is_authorized = (
        role in ["admin", "owner"]
        or project.leader_id == user_id
        or (project.is_public and deliverable.is_public)
    )
    if not is_authorized:
        return jsonify({"error": "No tienes permiso para ver este archivo."}), 403

    filename = os.path.basename(deliverable.file_path)
    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    return send_from_directory(uploads_dir, filename, as_attachment=False)


# Descarga el archivo con su nombre original. Mismas reglas de acceso que view
@deliverable_bp.route("/download/<int:deliverable_id>", methods=["GET"])
@login_required
def download_deliverable(deliverable_id: int) -> Response:
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    project = deliverable.project

    role = session.get("role")
    user_id = session.get("user_id")

    is_authorized = (
        role in ["admin", "owner"]
        or project.leader_id == user_id
        or (project.is_public and deliverable.is_public)
    )
    if not is_authorized:
        return jsonify({"error": "No tienes permiso para descargar este archivo."}), 403

    filename = os.path.basename(deliverable.file_path)

    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    return send_from_directory(uploads_dir, filename, as_attachment=True, download_name=deliverable.name + os.path.splitext(filename)[1])


# Sube un archivo a un proyecto. Espera multipart/form-data con file, name, description, is_public
@deliverable_bp.route("/upload/<int:project_id>", methods=["POST"])
@login_required
def upload_deliverable(project_id: int) -> Response:
    project = Project.query.get_or_404(project_id)
    role = session.get("role")

    # Solo permite subir si la convocatoria esta activa (excepto admin/owner)
    if role not in ["admin", "owner"] and project.call and not project.call.is_active:
        return jsonify({"error": _CALL_INACTIVE_MSG}), 403

    if project.leader_id != session.get("user_id"):
        return (
            jsonify(
                {"error": "No tienes permiso para subir archivos a este proyecto."}
            ),
            403,
        )

    if "file" not in request.files:
        return jsonify({"error": "No se encontró el archivo."}), 400

    file = request.files["file"]
    name = request.form.get("name")
    description = request.form.get("description")
    is_public = request.form.get("is_public") == "true"

    if not name or not description:
        return jsonify({"error": "Nombre y descripción son obligatorios."}), 400

    deliverable, error, status = DeliverableService.create(
        name, description, project_id, file, is_public=is_public
    )

    if error:
        return jsonify({"error": error}), status

    return (
        jsonify(
            {
                "message": "Archivo subido exitosamente.",
                "deliverable_id": deliverable.id,
            }
        ),
        201,
    )


# Alterna la visibilidad publica/privada de un archivo
@deliverable_bp.route("/<int:deliverable_id>/visibility", methods=["PATCH"])
@login_required
def toggle_file_visibility(deliverable_id: int) -> Response:
    role = session.get("role")
    if role not in ["admin", "owner"]:
        deliverable_obj = Deliverable.query.get(deliverable_id)
        if deliverable_obj and deliverable_obj.project.call and not deliverable_obj.project.call.is_active:
            return jsonify({"error": _CALL_INACTIVE_MSG}), 403

    deliverable, error, status = DeliverableService.toggle_visibility(
        deliverable_id=deliverable_id,
        user_id=session.get("user_id"),
        role=session.get("role"),
    )

    if error:
        return jsonify({"error": error}), status

    return jsonify({
        "message": "Visibilidad actualizada.",
        "is_public": deliverable.is_public,
    }), 200


# Actualiza nombre, descripcion o visibilidad de un archivo. Espera JSON
@deliverable_bp.route("/<int:deliverable_id>", methods=["PUT"])
@login_required
def update_deliverable(deliverable_id: int) -> Response:
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    project = deliverable.project
    role = session.get("role")

    if role not in ["admin", "owner"] and project.call and not project.call.is_active:
        return jsonify({"error": _CALL_INACTIVE_MSG}), 403

    if project.leader_id != session.get("user_id"):
        return jsonify({"error": "No tienes permiso para editar este archivo."}), 403

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name and not description and "is_public" not in data:
        return jsonify({"error": "Nada que actualizar."}), 400

    try:
        if name:
            deliverable.name = name
        if description:
            deliverable.description = description
        if "is_public" in data:
            deliverable.is_public = bool(data["is_public"])

        db.session.commit()
        return jsonify({"message": "Archivo actualizado exitosamente."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Elimina un archivo del proyecto y del disco. Solo leader del proyecto o admin/owner
@deliverable_bp.route("/<int:deliverable_id>", methods=["DELETE"])
@login_required
def delete_deliverable(deliverable_id: int) -> Response:
    deliverable = Deliverable.query.get_or_404(deliverable_id)

    role = session.get("role")
    project = deliverable.project
    is_leader = project.leader_id == session.get("user_id")

    if role not in ["admin", "owner"] and project.call and not project.call.is_active:
        return jsonify({"error": _CALL_INACTIVE_MSG}), 403

    if role not in ["admin", "owner"] and not is_leader:
        return (
            jsonify({"error": "No tienes permiso para eliminar este archivo."}),
            403,
        )

    try:
        # Elimina el archivo fisico del disco
        full_path = os.path.join(current_app.root_path, deliverable.file_path)
        if os.path.exists(full_path):
            os.remove(full_path)

        db.session.delete(deliverable)
        db.session.commit()
        return jsonify({"message": "Archivo eliminado exitosamente."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
