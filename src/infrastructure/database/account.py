from src.ext.database import db
from .base import BaseTable


class AccountTable(BaseTable):
    __tablename__ = "accounts"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    daily_withdrawal_limit = db.Column(db.Float, default=0.0)
    transactions = db.relationship("TransactionTable", backref="accounts", lazy=True)
