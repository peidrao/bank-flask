from datetime import datetime
from src.ext.database import db
from .base import BaseTable


class TransactionTable(BaseTable):
    __tablename__ = "transactions"

    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=False)
    value = db.Column(db.Float, default=0.0)
    type = db.Column(db.String(1), default="+")
