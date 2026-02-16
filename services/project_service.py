from datetime import datetime
from models import db, Project


class ProjectService:
    @staticmethod
    def create(name, description, leader_id, call_id):
        if not name or not name.strip():
            return None, "El nombre es obligatorio.", 422

        if not leader_id:
            return None, "El líder del proyecto es obligatorio.", 422

        if not call_id:
            return None, "La convocatoria del proyecto es obligatoria.", 422

        if Project.query.filter_by(name=name.strip()).first():
            return None, "Ya existe un proyecto con ese nombre.", 409

        if Project.query.filter_by(leader_id=leader_id, call_id=call_id).first():
            return None, "Solo puedes registrar un proyecto por convocatoria.", 409

        try:
            project = Project(
                name=name.strip(),
                description=description,
                leader_id=leader_id,
                call_id=call_id,
            )
            db.session.add(project)
            db.session.commit()
            return project, None, None
        except Exception as e:
            db.session.rollback()
            return None, "Error al crear el proyecto.", 500

    @staticmethod
    def get_all(user_id, role):
        if role in ["admin", "owner"]:
            return Project.query.all()
        return Project.query.filter_by(leader_id=user_id).all()

    @staticmethod
    def get_by_id(project_id):
        return Project.query.get(project_id)

    @staticmethod
    def update(project_id, user_id, role, **kwargs):
        project = Project.query.get(project_id)
        if not project:
            return None, "Proyecto no encontrado.", 404

        if role in ["admin", "owner"]:
            return None, "Los administradores no pueden editar proyectos.", 403

        if project.leader_id != user_id:
            return None, "No tienes permiso para editar este proyecto.", 403

        if "name" in kwargs:
            new_name = kwargs["name"].strip()
            existing = Project.query.filter(
                Project.name == new_name, Project.id != project_id
            ).first()
            if existing:
                return None, "Ya existe un proyecto con ese nombre.", 409
            project.name = new_name

        try:
            if "description" in kwargs:
                project.description = kwargs["description"]

            db.session.commit()
            return project, None, None
        except Exception as e:
            db.session.rollback()
            print(f"[ProjectService.update] {e}")
            return None, "Error al actualizar el proyecto.", 500

    @staticmethod
    def delete(project_id, user_id, role):
        project = Project.query.get(project_id)
        if not project:
            return None, "Proyecto no encontrado.", 404

        try:
            db.session.delete(project)
            db.session.commit()
            return project, None, None
        except Exception:
            db.session.rollback()
            return None, "Error al eliminar el proyecto.", 500
