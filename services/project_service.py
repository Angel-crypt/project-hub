from typing import Optional
from models import db, Project


class ProjectService:
    @staticmethod
    def create(
        name: str,
        description: str,
        leader_id: int,
        call_id: int,
        is_public: bool = False,
    ) -> tuple[Optional[Project], Optional[str], Optional[int]]:
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
                is_public=is_public,
            )
            db.session.add(project)
            db.session.commit()
            return project, None, None
        except Exception as e:
            db.session.rollback()
            return None, "Error al crear el proyecto.", 500

    @staticmethod
    def get_all(user_id: int, role: str) -> list[Project]:
        if role in ["admin", "owner"]:
            return Project.query.all()
        return Project.query.filter_by(leader_id=user_id).all()

    @staticmethod
    def get_by_id(project_id: int) -> Optional[Project]:
        return Project.query.get(project_id)

    @staticmethod
    def update(
        project_id: int,
        user_id: int,
        role: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_public: Optional[bool] = None,
    ) -> tuple[Optional[Project], Optional[str], Optional[int]]:
        project = Project.query.get(project_id)
        if not project:
            return None, "Proyecto no encontrado.", 404

        if role in ["admin", "owner"]:
            return None, "Los administradores no pueden editar proyectos.", 403

        if project.leader_id != user_id:
            return None, "No tienes permiso para editar este proyecto.", 403

        if name is not None:
            new_name = name.strip()
            existing = Project.query.filter(
                Project.name == new_name, Project.id != project_id
            ).first()
            if existing:
                return None, "Ya existe un proyecto con ese nombre.", 409
            project.name = new_name

        try:
            if description is not None:
                project.description = description
            if is_public is not None:
                project.is_public = is_public

            db.session.commit()
            return project, None, None
        except Exception as e:
            db.session.rollback()
            print(f"[ProjectService.update] {e}")
            return None, "Error al actualizar el proyecto.", 500

    @staticmethod
    def toggle_visibility(
        project_id: int, user_id: int, role: str
    ) -> tuple[Optional[Project], Optional[str], Optional[int]]:
        project = Project.query.get(project_id)
        if not project:
            return None, "Proyecto no encontrado.", 404

        if role not in ["admin", "owner"] and project.leader_id != user_id:
            return None, "No tienes permiso para cambiar la visibilidad.", 403

        try:
            project.is_public = not project.is_public
            db.session.commit()
            return project, None, None
        except Exception as e:
            db.session.rollback()
            return None, "Error al cambiar la visibilidad.", 500

    @staticmethod
    def get_public() -> list[Project]:
        return Project.query.filter_by(is_public=True).all()

    @staticmethod
    def delete(
        project_id: int, user_id: int, role: str
    ) -> tuple[Optional[Project], Optional[str], Optional[int]]:
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
