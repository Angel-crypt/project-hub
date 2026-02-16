from models import db, User, RoleEnum


class AuthService:
    @staticmethod
    def register(enrrollment_number, name, password):
        enrrollment_number = enrrollment_number.strip().upper() if enrrollment_number else ""

        if not enrrollment_number or len(enrrollment_number) > 10:
            return None, "Matrícula inválida (máx. 10 caracteres).", 422

        if not name:
            return None, "El nombre es obligatorio.", 422

        if not password or len(password) < 6:
            return None, "La contraseña debe tener al menos 6 caracteres.", 422

        if User.query.filter_by(enrrollment_number=enrrollment_number).first():
            return None, "No se pudo completar el registro.", 409

        try:
            user = User(
                enrrollment_number=enrrollment_number,
                name=name,
                password=password,
                role=RoleEnum.LEADER,
            )
            db.session.add(user)
            db.session.commit()
            return user, None, None
        except Exception:
            db.session.rollback()
            return None, "Error al registrar usuario.", 500

    @staticmethod
    def login(enrrollment_number, password):
        enrrollment_number = enrrollment_number.strip().upper() if enrrollment_number else ""
        user = User.query.filter_by(enrrollment_number=enrrollment_number).first()

        if not user or not user.check_password(password):
            return None, "Matrícula o contraseña incorrecta.", 401

        return user, None, None
