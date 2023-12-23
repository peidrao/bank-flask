from werkzeug.security import generate_password_hash
from src.ext.database import db


class PersonTable(db.Model):
    __tablename__ = "persons"

    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    cpf = db.Column(db.String(20), nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    accounts = db.relationship("AccountTable", backref="persons", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
