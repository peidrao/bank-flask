from typing import Optional
from sqlalchemy import select


from src.domain.entities import Bank
from src.infrastructure.database import BankTable


class BankRepository:
    def __init__(self, session=None):
        self.session = session

    def get(self, **kwargs) -> Optional[Bank | None]:
        query = select(BankTable).where(BankTable.compe == kwargs.get("compe"))
        bank_db = self.session.execute(query).first()
        return bank_db
