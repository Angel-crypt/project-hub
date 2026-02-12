from models import db
from datetime import datetime


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    leader_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    call_id = db.Column(db.Integer, db.ForeignKey("calls.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    leader = db.relationship("User", backref="projects", lazy=True)

    def __init__(self, name, description, leader_id, call_id):
        self.name = name
        self.description = description
        self.leader_id = leader_id
        self.call_id = call_id

    def __repr__(self):
        return f"<Proyecto {self.name}>"
