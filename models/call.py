from models import db
from datetime import datetime


class Call(db.Model):
    __tablename__ = "calls"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    opening_date = db.Column(db.DateTime, nullable=False)
    closing_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projects = db.relationship("Project", backref="call", lazy=True)

    def __init__(self, title, description, opening_date, closing_date):
        self.title = title
        self.description = description
        self.opening_date = opening_date
        self.closing_date = closing_date

    def __repr__(self):
        return f"<Convocatoria {self.title}>"
