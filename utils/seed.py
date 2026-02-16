from models import db, User, RoleEnum

DEFAULT_USERS = [
    {
        "enrrollment_number": "OWNER001",
        "name": "Owner",
        "password": "owner123",
        "role": RoleEnum.OWNER,
    },
    {
        "enrrollment_number": "ADMIN001",
        "name": "Admin",
        "password": "admin123",
        "role": RoleEnum.ADMIN,
    },
    {
        "enrrollment_number": "LEADER001",
        "name": "Leader",
        "password": "leader123",
        "role": RoleEnum.LEADER,
    },
]


def seed_users():
    for data in DEFAULT_USERS:
        if not User.query.filter_by(enrrollment_number=data["enrrollment_number"]).first():
            db.session.add(User(**data))
    db.session.commit()
