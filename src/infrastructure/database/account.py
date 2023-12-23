from datetime import datetime
from src.ext.database import db


class AccountTable(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), nullable=False)
    amount = db.Column(db.Float, default=0.0)
    daily_withdrawal_limit = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    account_type = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    transactions = db.relationship("TransactionTable", backref="accounts", lazy=True)
