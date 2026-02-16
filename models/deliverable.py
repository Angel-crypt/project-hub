from models import db
from datetime import datetime


class Deliverable(db.Model):
    __tablename__ = "deliverables"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80, collation="NOCASE"), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    project = db.relationship("Project", backref="deliverables", lazy=True)

    def __init__(self, name, description, file_path, project_id):
        self.name = name
        self.description = description
        self.file_path = file_path
        self.project_id = project_id

    def __repr__(self):
        return f"<Entregable {self.title}>"
