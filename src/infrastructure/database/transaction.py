from datetime import datetime
from src.ext.database import db


class TransactionTable(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    value = db.Column(db.Float, default=0.0)
    type = db.Column(db.String(1), default="+")
    transaction_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
