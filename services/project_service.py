from models import db, Project, Call, User


class ProjectService:
    @staticmethod
    def create(name, description, leader_id, call_id):
        if not name or not name.strip():
            return None, "El nombre del proyecto es obligatorio.", 422

        if not User.query.get(leader_id):
            return None, "El líder asignado no existe.", 422

        if not Call.query.get(call_id):
            return None, "La convocatoria no existe.", 422

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
        except Exception:
            db.session.rollback()
            return None, "Error al crear el proyecto.", 500

    @staticmethod
    def get_all():
        return Project.query.all()

    @staticmethod
    def get_by_id(project_id):
        return Project.query.get(project_id)

    @staticmethod
    def get_by_call(call_id):
        return Project.query.filter_by(call_id=call_id).all()

    @staticmethod
    def get_by_leader(leader_id):
        return Project.query.filter_by(leader_id=leader_id).all()

    @staticmethod
    def update(project_id, **kwargs):
        project = Project.query.get(project_id)
        if not project:
            return None, "Proyecto no encontrado.", 404

        try:
            if "name" in kwargs:
                project.name = kwargs["name"].strip()
            if "description" in kwargs:
                project.description = kwargs["description"]
            if "leader_id" in kwargs:
                if not User.query.get(kwargs["leader_id"]):
                    return None, "El líder asignado no existe.", 422
                project.leader_id = kwargs["leader_id"]
            if "call_id" in kwargs:
                if not Call.query.get(kwargs["call_id"]):
                    return None, "La convocatoria no existe.", 422
                project.call_id = kwargs["call_id"]

            db.session.commit()
            return project, None, None
        except Exception:
            db.session.rollback()
            return None, "Error al actualizar el proyecto.", 500

    @staticmethod
    def delete(project_id):
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
