from models import db, User, RoleEnum


class UserService:
    @staticmethod
    def create(enrollment_number , name, password, role="leader"):
        enrollment_number  = enrollment_number .strip().upper() if enrollment_number  else ""

        if not enrollment_number  or len(enrollment_number ) > 10:
            return None, "Matrícula inválida (máx. 10 caracteres).", 422

        if not name:
            return None, "El nombre es obligatorio.", 422

        if not password or len(password) < 6:
            return None, "La contraseña debe tener al menos 6 caracteres.", 422

        if User.query.filter_by(enrollment_number =enrollment_number ).first():
            return None, "No se pudo completar el registro.", 409

        try:
            role_enum = RoleEnum.ADMIN if role == "admin" else RoleEnum.LEADER
            user = User(
                enrollment_number =enrollment_number ,
                name=name,
                password=password,
                role=role_enum,
            )
            db.session.add(user)
            db.session.commit()
            return user, None, None
        except Exception:
            db.session.rollback()
            return None, "Error al crear usuario.", 500

    @staticmethod
    def get_admins():
        return User.query.filter_by(role=RoleEnum.ADMIN).all()

    @staticmethod
    def get_leaders():
        return User.query.filter_by(role=RoleEnum.LEADER).all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_enrollment(enrollment_number ):
        return User.query.filter_by(enrollment_number =enrollment_number ).first()

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
