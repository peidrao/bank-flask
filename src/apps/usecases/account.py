from flask import jsonify
from src.domain.entities import AccountDeposit, Account, Transaction
from src.infrastructure.repositories import UserRepository, AccountRepository
from src.infrastructure.repositories.transaction import TransactionRepository


class AccountUpdateUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        account_repository: AccountRepository,
    ):
        self.user_repository = user_repository
        self.account_repository = account_repository

    def __call__(self, account_id: int, user_id, **kwargs):
        account = self.account_repository.get_by_args(
            id=account_id, user_id=user_id
        )

        if not account:
            return

        account_blocked = self.account_repository.update_account(
            account_id=account.id, **kwargs
        )

        return jsonify(account_blocked)


class AccountDepositUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
    ):
        self.user_repository = user_repository
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def __call__(self, account: AccountDeposit):
        account_db = self.account_repository.get_by_args(id=account.account)

        if not account_db:
            return

        account_updated = self.account_repository.update_account(
            account_id=account_db.id,
            amount=account_db.amount + account.value,
        )

        self.transaction_repository.create(
            Transaction(account_id=account_db.id, value=account.value, type="+")
        )

        return jsonify(account_updated)


class AccountCreateUseCase:
    def __init__(
        self,
        account_repository: AccountRepository,
    ):
        self.account_repository = account_repository

    def __call__(self, account: Account):
        new_account = self.account_repository.create(account)

        response = jsonify(new_account)
        response.status_code = 201

        return response


class AccountGetUseCase:
    def __init__(
        self,
        account_repository: AccountRepository,
    ):
        self.account_repository = account_repository

    def __call__(
        self,
        account_id: int,
        user_id: int,
    ):
        account_db = self.account_repository.get_by_args(
            id=account_id, user_id=user_id
        )

        if not account_db:
            return

        return jsonify(account_db)


class AccountWithdrawUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
    ):
        self.user_repository = user_repository
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def __call__(self, account: AccountDeposit, user_id: int):
        account_db = self.account_repository.get_by_args(id=account.account)

        total_value_transactions_by_account = (
            self.transaction_repository.get_aggregate_value_in_one_day(
                account_id=account_db.id
            )
        )

        if (
            total_value_transactions_by_account >= account_db.daily_withdrawal_limit
            or account.value > account_db.daily_withdrawal_limit
        ):
            return {
                "error": "Não é possível realizar saques, você está excedendo o limite diário"
            }, 400

        if (
            account_db.amount < account.value
            or account.value + total_value_transactions_by_account
            > account_db.daily_withdrawal_limit
        ):
            return {"error": "Sem saldo disponível para realizar saque"}, 400

        self.transaction_repository.create(
            Transaction(
                account_id=account_db.id,
                value=account.value,
                type="-",
            )
        )
        new_amount = account_db.amount - account.value
        account_updated = self.account_repository.update_account(
            account_id=account_db.id, amount=new_amount
        )

        response = jsonify(account_updated)
        response.status_code = 201

        return response


class AccountsMeUseCase:
    def __init__(
        self,
        account_repository: AccountRepository,
    ):
        self.account_repository = account_repository

    def __call__(
        self,
        user_id: int,
    ):
        account_db = self.account_repository.filter(user_id=user_id)

        if not account_db:
            return []

        return jsonify(account_db)


class AccountTransactionsUseCase:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
    ):
        self.transaction_repository = transaction_repository

    def __call__(
        self,
        user_id: int,
        account_id: int,
    ):
        account_db = self.transaction_repository.filter_transactions_by_account(
            user_id=user_id,
            account_id=account_id,
        )

        if not account_db:
            return

        return jsonify(account_db)
