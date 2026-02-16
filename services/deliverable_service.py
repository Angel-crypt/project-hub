from models import db
from models.deliverable import Deliverable
from werkzeug.utils import secure_filename
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
    def allowed_file(filename):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @staticmethod
    def validate_file_content(file):
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
    def create(name, description, project_id, file):
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
            )

            db.session.add(new_deliverable)
            db.session.commit()
            return new_deliverable, None, 201

        except Exception as e:
            db.session.rollback()
            return None, str(e), 500

    @staticmethod
    def get_by_project(project_id):
        return Deliverable.query.filter_by(project_id=project_id).all()
