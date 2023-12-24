from werkzeug.security import generate_password_hash
from src.ext.database import db
from .base import BaseTable


class UserTable(BaseTable):
    __tablename__ = "users"

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    cpf = db.Column(db.String(20), nullable=True)
    accounts = db.relationship("AccountTable", backref="users", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
