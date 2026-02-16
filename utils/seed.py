from operator import call
from models import db, User, RoleEnum, Call
from datetime import datetime

DEFAULT_USERS = [
    {
        "enrollment_number": "OWNER001",
        "name": "Owner",
        "password": "owner123",
        "role": RoleEnum.OWNER,
    },
    {
        "enrollment_number": "ADMIN001",
        "name": "Admin",
        "password": "admin123",
        "role": RoleEnum.ADMIN,
    },
    {
        "enrollment_number": "LEADER001",
        "name": "Leader",
        "password": "leader123",
        "role": RoleEnum.LEADER,
    },
]

DEFAULT_CALLS = [
    {
        "title": "Convocatoria de Proyectos 2026",
        "description": "Abierta para propuestas de proyectos innovadores en tecnología y sostenibilidad.",
        "opening_date": "2026-01-01",
        "closing_date": "2026-02-28",
    },
    {
        "title": "Becas de Investigación Q1 2026",
        "description": "Programa de becas para proyectos de investigación en ciencias aplicadas.",
        "opening_date": "2026-01-15",
        "closing_date": "2026-03-15",
    },
    {
        "title": "Hackathon Universitario 2026",
        "description": "Competencia de desarrollo de software orientada a soluciones educativas.",
        "opening_date": "2026-02-01",
        "closing_date": "2026-02-15",
    },
]


def seed_users():
    for user_data in DEFAULT_USERS:
        if not User.query.filter_by(enrollment_number=user_data["enrollment_number"]).first():
            db.session.add(User(**user_data))
    
    db.session.commit()

def seed_calls():
    for call_data in DEFAULT_CALLS:
        call_data["opening_date"] = datetime.strptime(call_data["opening_date"], "%Y-%m-%d")
        call_data["closing_date"] = datetime.strptime(call_data["closing_date"], "%Y-%m-%d")
        if not Call.query.filter_by(title=call_data["title"]).first():
            db.session.add(Call(**call_data))
    
    db.session.commit()