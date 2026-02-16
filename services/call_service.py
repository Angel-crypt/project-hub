from datetime import datetime
from models import db, Call


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.strptime(value, "%Y-%m-%d")


class CallService:
    @staticmethod
    def create(title, description, opening_date, closing_date):
        if not title or not title.strip():
            return None, "El título es obligatorio.", 422

        if not opening_date or not closing_date:
            return None, "Las fechas de apertura y cierre son obligatorias.", 422

        parsed_opening = _parse_date(opening_date)
        parsed_closing = _parse_date(closing_date)

        if parsed_opening >= parsed_closing:
            return None, "La fecha de apertura debe ser anterior a la de cierre.", 422

        if Call.query.filter_by(title=title.strip()).first():
            return None, "Ya existe una convocatoria con ese título.", 409

        try:
            call = Call(
                title=title.strip(),
                description=description,
                opening_date=parsed_opening,
                closing_date=parsed_closing,
            )
            db.session.add(call)
            db.session.commit()
            return call, None, None
        except Exception as e:
            db.session.rollback()
            return None, "Error al crear la convocatoria.", 500

    @staticmethod
    def get_all():
        return Call.query.all()

    @staticmethod
    def get_by_id(call_id):
        return Call.query.get(call_id)

    @staticmethod
    def update(call_id, **kwargs):
        call = Call.query.get(call_id)
        if not call:
            return None, "Convocatoria no encontrada.", 404

        if "title" in kwargs:
            new_title = kwargs["title"].strip()
            existing = Call.query.filter(
                Call.title == new_title, Call.id != call_id
            ).first()
            if existing:
                return None, "Ya existe una convocatoria con ese título.", 409
            call.title = new_title

        try:
            if "description" in kwargs:
                call.description = kwargs["description"]
            if "opening_date" in kwargs:
                call.opening_date = _parse_date(kwargs["opening_date"])
            if "closing_date" in kwargs:
                call.closing_date = _parse_date(kwargs["closing_date"])

            db.session.commit()
            return call, None, None
        except Exception as e:
            db.session.rollback()
            print(f"[CallService.update] {e}")
            return None, "Error al actualizar la convocatoria.", 500

    @staticmethod
    def delete(call_id):
        call = Call.query.get(call_id)
        if not call:
            return None, "Convocatoria no encontrada.", 404

        if call.projects:
            return (
                None,
                "No se puede eliminar una convocatoria con proyectos asociados.",
                409,
            )

        try:
            db.session.delete(call)
            db.session.commit()
            return call, None, None
        except Exception:
            db.session.rollback()
            return None, "Error al eliminar la convocatoria.", 500
