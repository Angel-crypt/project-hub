from models import db, User, RoleEnum


class AuthService:
    @staticmethod
    def register(enrrollment_number, name, password, role="leader"):
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
            role_enum = RoleEnum.ADMIN if role == "admin" else RoleEnum.LEADER
            user = User(
                enrrollment_number=enrrollment_number,
                name=name,
                password=password,
                role=role_enum,
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

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_enrollment(enrrollment_number):
        return User.query.filter_by(enrrollment_number=enrrollment_number).first()

    @staticmethod
    def update(user_id, **kwargs):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuario no encontrado.", 404

        try:
            if "name" in kwargs:
                user.name = kwargs["name"]
            if "password" in kwargs:
                user.set_password(kwargs["password"])
            if "role" in kwargs:
                user.role = kwargs["role"]

            db.session.commit()
            return user, None, None
        except Exception:
            db.session.rollback()
            return None, "Error al actualizar usuario.", 500

    @staticmethod
    def delete(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuario no encontrado.", 404

        try:
            db.session.delete(user)
            db.session.commit()
            return user, None, None
        except Exception:
            db.session.rollback()
            return None, "Error al eliminar usuario.", 500
