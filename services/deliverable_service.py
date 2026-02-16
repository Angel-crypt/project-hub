from typing import Optional
from models import db
from models.deliverable import Deliverable
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import uuid

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx"}
UPLOAD_FOLDER = "static/uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024

FILE_SIGNATURES = {
    "pdf": b"%PDF",
    "png": b"\x89PNG\r\n\x1a\n",
    "jpg": b"\xff\xd8\xff",
    "jpeg": b"\xff\xd8\xff",
    "doc": b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",
    "docx": b"PK\x03\x04",
}


class DeliverableService:
    @staticmethod
    def allowed_file(filename: str) -> bool:
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @staticmethod
    def validate_file_content(file: FileStorage) -> bool:
        filename = file.filename
        ext = filename.rsplit(".", 1)[1].lower()

        if ext not in FILE_SIGNATURES:
            return True

        required_signature = FILE_SIGNATURES[ext]

        header = file.read(len(required_signature))
        file.seek(0)

        return header.startswith(required_signature) or (
            ext == "doc" and header.startswith(b"\xd0\xcf\x11\xe0")
        )

    @staticmethod
    def create(
        name: str,
        description: str,
        project_id: int,
        file: FileStorage,
        is_public: bool = False,
    ) -> tuple[Optional[Deliverable], Optional[str], Optional[int]]:
        if not file or file.filename == "":
            return None, "No se ha seleccionado ningún archivo.", 400

        if not DeliverableService.allowed_file(file.filename):
            return None, "Tipo de archivo no permitido.", 400

        if not DeliverableService.validate_file_content(file):
            return (
                None,
                "El contenido del archivo no coincide con su extensión o está dañado.",
                400,
            )

        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)

        if file_length > MAX_FILE_SIZE:
            return None, "El archivo excede el tamaño máximo permitido (10MB).", 400

        try:
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            original_filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

            file.save(file_path)

            relative_path = f"uploads/{unique_filename}"

            new_deliverable = Deliverable(
                name=name,
                description=description,
                file_path=relative_path,
                project_id=project_id,
                is_public=is_public,
            )

            db.session.add(new_deliverable)
            db.session.commit()
            return new_deliverable, None, 201

        except Exception as e:
            db.session.rollback()
            return None, str(e), 500

    @staticmethod
    def toggle_visibility(
        deliverable_id: int, user_id: int, role: str
    ) -> tuple[Optional[Deliverable], Optional[str], Optional[int]]:
        deliverable = Deliverable.query.get(deliverable_id)
        if not deliverable:
            return None, "Archivo no encontrado.", 404

        if role not in ["admin", "owner"] and deliverable.project.leader_id != user_id:
            return None, "No tienes permiso para cambiar la visibilidad.", 403

        try:
            deliverable.is_public = not deliverable.is_public
            db.session.commit()
            return deliverable, None, None
        except Exception as e:
            db.session.rollback()
            return None, "Error al cambiar la visibilidad.", 500

    @staticmethod
    def get_by_project(project_id: int) -> list[Deliverable]:
        return Deliverable.query.filter_by(project_id=project_id).all()
