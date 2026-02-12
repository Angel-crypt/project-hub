from models import db, User, RoleEnum


class AuthService:
    @staticmethod
    def register(enrrollment_number, name, password, role="leader"):
        enrrollment_number = enrrollment_number.strip().upper() if enrrollment_number else ""
        existing = User.query.filter_by(enrrollment_number=enrrollment_number).first()
        if existing:
            return None, "No se pudo completar el registro.", 400

        if not enrrollment_number or len(enrrollment_number) > 10:
            return None, "Matrícula inválida (máx. 10 caracteres).", 400

        if not name:
            return None, "El nombre es obligatorio.", 400

        if not password or len(password) < 6:
            return None, "La contraseña debe tener al menos 6 caracteres.", 400

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

    @staticmethod
    def login(enrrollment_number, password):
        enrrollment_number = enrrollment_number.strip().upper() if enrrollment_number else ""
        user = User.query.filter_by(enrrollment_number=enrrollment_number).first()

        if not user or not user.check_password(password):
            return None, "Matrícula o contraseña incorrecta.", 401

        return user, None, None

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_by_enrollment(enrrollment_number):
        return User.query.filter_by(enrrollment_number=enrrollment_number).first()

    @staticmethod
    def update_user(user_id, **kwargs):
        user = User.query.get(user_id)
        if not user:
            return None, "Usuario no encontrado."

        if "name" in kwargs:
            user.name = kwargs["name"]
        if "password" in kwargs:
            user.set_password(kwargs["password"])
        if "role" in kwargs:
            user.role = kwargs["role"]

        db.session.commit()
        return user, None

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return False, "Usuario no encontrado."

        db.session.delete(user)
        db.session.commit()
        return True, None
