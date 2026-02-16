from flask import Blueprint, request, jsonify, session, current_app, send_from_directory
from services.deliverable_service import DeliverableService
from models.project import Project
from models.deliverable import Deliverable
from models import db
from utils.decorators import login_required
import os

deliverable_bp = Blueprint("deliverable", __name__, url_prefix="/deliverable")

@deliverable_bp.route("/view/<int:deliverable_id>", methods=["GET"])
@login_required
def view_deliverable(deliverable_id):
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    project = deliverable.project

    role = session.get("role")
    user_id = session.get("user_id")

    if role not in ["admin", "owner"] and project.leader_id != user_id:
        return jsonify({"error": "No tienes permiso para ver este archivo."}), 403


    filename = os.path.basename(deliverable.file_path)
    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    return send_from_directory(uploads_dir, filename, as_attachment=False)


@deliverable_bp.route("/download/<int:deliverable_id>", methods=["GET"])
@login_required
def download_deliverable(deliverable_id):
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    project = deliverable.project

    role = session.get("role")
    user_id = session.get("user_id")

    if role not in ["admin", "owner"] and project.leader_id != user_id:
        return jsonify({"error": "No tienes permiso para descargar este archivo."}), 403

    filename = os.path.basename(deliverable.file_path)

    uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    return send_from_directory(uploads_dir, filename, as_attachment=True, download_name=deliverable.name + os.path.splitext(filename)[1])



@deliverable_bp.route("/upload/<int:project_id>", methods=["POST"])
@login_required
def upload_deliverable(project_id):
    project = Project.query.get_or_404(project_id)
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

    if not name or not description:
        return jsonify({"error": "Nombre y descripción son obligatorios."}), 400

    deliverable, error, status = DeliverableService.create(
        name, description, project_id, file
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


@deliverable_bp.route("/<int:deliverable_id>", methods=["PUT"])
@login_required
def update_deliverable(deliverable_id):
    deliverable = Deliverable.query.get_or_404(deliverable_id)
    project = deliverable.project

    if project.leader_id != session.get("user_id"):
        return jsonify({"error": "No tienes permiso para editar este archivo."}), 403

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")

    if not name and not description:
        return jsonify({"error": "Nada que actualizar."}), 400

    try:
        if name:
            deliverable.name = name
        if description:
            deliverable.description = description

        db.session.commit()
        return jsonify({"message": "Archivo actualizado exitosamente."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@deliverable_bp.route("/<int:deliverable_id>", methods=["DELETE"])
@login_required
def delete_deliverable(deliverable_id):
    deliverable = Deliverable.query.get_or_404(deliverable_id)

    role = session.get("role")
    project = deliverable.project
    is_leader = project.leader_id == session.get("user_id")

    if role not in ["admin", "owner"] and not is_leader:
        return (
            jsonify({"error": "No tienes permiso para eliminar este archivo."}),
            403,
        )

    try:
        full_path = os.path.join(current_app.root_path, deliverable.file_path)
        if os.path.exists(full_path):
            os.remove(full_path)

        db.session.delete(deliverable)
        db.session.commit()
        return jsonify({"message": "Archivo eliminado exitosamente."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
