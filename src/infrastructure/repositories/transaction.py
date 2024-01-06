from datetime import date, datetime
from itertools import islice
from typing import List, Tuple

from sqlalchemy import desc

from src.infrastructure.database import TransactionTable
from src.domain.entities import Transaction
from src.infrastructure.database.account import AccountTable
from src.infrastructure.database.user import UserTable


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
            .filter(TransactionTable.created_at.between(start_of_day, end_of_day))
            .all()
        )

        total_value = sum(transaction.value for transaction in transactions)
        return total_value

    def __filter_transactions_by_person(
        self,
        user_id: int,
    ) -> List[TransactionTable | None]:
        transactions_db = (
            TransactionTable.query.join(
                AccountTable, AccountTable.id == TransactionTable.account_id
            )
            .join(UserTable, UserTable.id == AccountTable.user_id)
            .filter(UserTable.id == user_id)
            .order_by(desc(TransactionTable.created_at))
            .all()
        )

        return transactions_db

    def filter_transactions_by_person(
        self, user_id: int
    ) -> Tuple[List[TransactionTable] | None, int, int]:
        transactions_db = self.__filter_transactions_by_person(user_id)
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
                created_at=transaction.created_at,
            )
            for transaction in transactions_db
        ]

        return transactions, transactions_cash_in, transactions_cash_out

    def get_last_transactions(
        self, user_id: int, limit: int
    ) -> List[Transaction | None]:
        transactions_db = self.__filter_transactions_by_person(user_id=user_id)
        if not transactions_db:
            return None

        transactions = [
            Transaction(
                id=transaction.id,
                account_id=transaction.account_id,
                value=transaction.value,
                type=transaction.type,
                created_at=transaction.created_at,
            )
            for transaction in transactions_db
            if transaction.type == "-"
        ]

        return list(islice(transactions, limit))

    def filter_transactions_by_account(
        self, user_id: int, account_id: int
    ) -> List[Transaction | None]:
        transactions_db = self.__filter_transactions_by_person(user_id=user_id)

        transactions = [
            Transaction(
                id=transaction.id,
                account_id=transaction.account_id,
                value=transaction.value,
                type=transaction.type,
                created_at=transaction.created_at,
            )
            for transaction in transactions_db
            if transaction.account_id == account_id
        ]

        return transactions
