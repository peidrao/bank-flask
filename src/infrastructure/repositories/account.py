from typing import List, Optional, Tuple

from src.infrastructure.database import AccountTable
from src.domain.entities import Account


class AccountRepository:
    def __init__(self, session=None):
        self.session = session

    def create(self, account: Account) -> Account:
        account_db = AccountTable(
            person_id=account.person_id,
            account_type=account.account_type,
            daily_withdrawal_limit=account.daily_withdrawal_limit,
        )
        self.session.add(account_db)
        self.session.commit()
        account.id = account_db.id
        account.created_at = account_db.created_at
        return account

    def get_by_person_id(self, person_id: int) -> Optional[Account]:
        account_db = AccountTable.query.filter_by(person_id=person_id).first()
        if not account_db:
            return None
        account = Account(
            id=account_db.id,
            amount=account_db.amount,
            person_id=account_db.person_id,
            daily_withdrawal_limit=account_db.daily_withdrawal_limit,
            is_active=account_db.is_active,
            account_type=account_db.account_type,
            created_at=account_db.created_at,
        )
        return account

    def get_by_args(self, *args, **kwargs) -> Optional[Account]:
        account_db = AccountTable.query.filter_by(**kwargs).first()
        if not account_db:
            return None
        account = Account(
            id=account_db.id,
            amount=account_db.amount,
            person_id=account_db.person_id,
            daily_withdrawal_limit=account_db.daily_withdrawal_limit,
            is_active=account_db.is_active,
            account_type=account_db.account_type,
            created_at=account_db.created_at,
        )
        return account

    def filter(self, *args, **kwargs) -> List[Account | None]:
        accounts_db = AccountTable.query.filter_by(**kwargs).all()

        if not accounts_db:
            return []

        accounts = [
            Account(
                id=account.id,
                person_id=account.person_id,
                amount=account.amount,
                daily_withdrawal_limit=account.daily_withdrawal_limit,
                is_active=account.is_active,
                account_type=account.account_type,
                created_at=account.created_at,
            )
            for account in accounts_db
        ]

        return accounts

    def update_account(self, account_id: int, **kwargs) -> Optional[Account]:
        account_db = AccountTable.query.filter_by(id=account_id).first()
        if not account_db:
            return None

        for key, value in kwargs.items():
            setattr(account_db, key, value)
        self.session.add(account_db)
        self.session.flush()
        self.session.commit()

        account = Account(
            id=account_db.id,
            amount=account_db.amount,
            person_id=account_db.person_id,
            daily_withdrawal_limit=account_db.daily_withdrawal_limit,
            is_active=account_db.is_active,
            account_type=account_db.account_type,
            created_at=account_db.created_at,
        )
        return account

    def get_accounts_info(self, person_id: int) -> Tuple[float, int]:
        accounts_db = AccountTable.query.filter_by(person_id=person_id).all()

        if not accounts_db:
            return 0, 0

        accounts_amount = sum(account.amount for account in accounts_db)

        return accounts_amount, len(accounts_db)
