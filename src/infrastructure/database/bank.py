from src.ext.database import db
from .base import BaseTable


class BankTable(BaseTable):
    __tablename__ = "banks"

    compe = db.Column(db.String(3))
    ispb = db.Column(db.String(8))
    document = db.Column(db.String(18))
    long_name = db.Column(db.String(200))
    short_name = db.Column(db.String(100))
