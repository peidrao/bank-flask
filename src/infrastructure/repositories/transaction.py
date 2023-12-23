from datetime import date, datetime
from itertools import islice
from typing import List, Tuple

from sqlalchemy import desc

from src.infrastructure.database import TransactionTable
from src.domain.entities import Transaction
from src.infrastructure.database.account import AccountTable
from src.infrastructure.database.person import PersonTable


class TransactionRepository:
    def __init__(self, session=None):
        self.session = session

    def create(self, transaction: Transaction) -> Transaction:
        transaction_db = TransactionTable(
            account_id=transaction.account_id,
            value=transaction.value,
            type=transaction.type,
        )
        self.session.add(transaction_db)
        self.session.commit()
        transaction.id = transaction_db.id
        return transaction

    def get_aggregate_value_in_one_day(self, account_id: int) -> float:
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        transactions = (
            self.session.query(TransactionTable)
            .filter(TransactionTable.account_id == account_id)
            .filter(TransactionTable.type == "-")
            .filter(TransactionTable.transaction_date.between(start_of_day, end_of_day))
            .all()
        )

        total_value = sum(transaction.value for transaction in transactions)
        return total_value

    def __filter_transactions_by_person(
        self,
        person_id: int,
    ) -> List[TransactionTable | None]:
        transactions_db = (
            TransactionTable.query.join(
                AccountTable, AccountTable.id == TransactionTable.account_id
            )
            .join(PersonTable, PersonTable.id == AccountTable.person_id)
            .filter(PersonTable.id == person_id)
            .order_by(desc(TransactionTable.transaction_date))
            .all()
        )

        return transactions_db

    def filter_transactions_by_person(
        self, person_id: int
    ) -> Tuple[List[TransactionTable] | None, int, int]:
        transactions_db = self.__filter_transactions_by_person(person_id)
        if not transactions_db:
            return None, 0, 0

        transactions_cash_in = sum(
            transaction.type == "+" for transaction in transactions_db
        )
        transactions_cash_out = len(transactions_db) - transactions_cash_in

        transactions = [
            Transaction(
                id=transaction.id,
                account_id=transaction.account_id,
                value=transaction.value,
                type=transaction.type,
                transaction_date=transaction.transaction_date,
            )
            for transaction in transactions_db
        ]

        return transactions, transactions_cash_in, transactions_cash_out

    def get_last_transactions(
        self, person_id: int, limit: int
    ) -> List[Transaction | None]:
        transactions_db = self.__filter_transactions_by_person(person_id=person_id)
        if not transactions_db:
            return None

        transactions = [
            Transaction(
                id=transaction.id,
                account_id=transaction.account_id,
                value=transaction.value,
                type=transaction.type,
                transaction_date=transaction.transaction_date,
            )
            for transaction in transactions_db
            if transaction.type == "-"
        ]

        return list(islice(transactions, limit))

    def filter_transactions_by_account(
        self, person_id: int, account_id: int
    ) -> List[Transaction | None]:
        transactions_db = self.__filter_transactions_by_person(person_id=person_id)

        transactions = [
            Transaction(
                id=transaction.id,
                account_id=transaction.account_id,
                value=transaction.value,
                type=transaction.type,
                transaction_date=transaction.transaction_date,
            )
            for transaction in transactions_db
            if transaction.account_id == account_id
        ]

        return transactions
