from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from src.apps.api.adapters import AccountOperationsRequestAdapter, AccountRequestAdapter
from src.domain.entities.account import Account
from src.infrastructure.repositories import (
    UserRepository,
    AccountRepository,
    TransactionRepository,
)
from src.apps.usecases import (
    AccountUpdateUseCase,
    AccountDepositUseCase,
    AccountCreateUseCase,
    AccountGetUseCase,
    AccountWithdrawUseCase,
    AccountsMeUseCase,
    AccountTransactionsUseCase,
)
from src.domain.entities import AccountDeposit

from src.ext.database import db


class AccountResource(Resource):
    @jwt_required()
    def post(self):
        try:
            adapter = AccountRequestAdapter()
            data = adapter.load(request.json)
        except ValidationError as e:
            return {"message": str(e)}, 400

        current_user = get_jwt_identity()
        daily_withdrawal_limit = data.get("daily_withdrawal_limit", None)
        user_id = current_user.get("id")

        new_account = Account(
            daily_withdrawal_limit=daily_withdrawal_limit,
            user_id=user_id,
            is_active=True,
            amount=0.0,
        )

        account_usecase = AccountCreateUseCase(
            account_repository=AccountRepository(db.session),
        )
        return account_usecase(account=new_account)


class AccountsMeResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        accounts_usecase = AccountsMeUseCase(
            account_repository=AccountRepository(db.session),
        )
        return accounts_usecase(user_id=current_user.get("id"))


class AccountDetailResource(Resource):
    @jwt_required()
    def get(self, account_id: int):
        current_user = get_jwt_identity()

        account_usecase = AccountGetUseCase(
            account_repository=AccountRepository(db.session),
        )
        return account_usecase(
            account_id=account_id, user_id=current_user.get("id")
        )

    @jwt_required()
    def patch(self, account_id: int):
        try:
            adapter = AccountRequestAdapter()
            data = adapter.load(request.json)
        except ValidationError as e:
            return {"message": str(e)}, 400

        current_user = get_jwt_identity()

        account = AccountUpdateUseCase(
            user_repository=UserRepository(db.session),
            account_repository=AccountRepository(db.session),
        )
        return account(
            account_id=account_id, user_id=current_user.get("id"), **data
        )


class AccountDepositResource(Resource):
    @jwt_required()
    def patch(self):
        try:
            adapter = AccountOperationsRequestAdapter()
            data = adapter.load(request.json)
        except ValidationError as e:
            return {"message": str(e)}, 400

        value = data.get("value", None)
        account = data.get("account", None)

        account_deposit = AccountDeposit(value=value, account=account)

        account_usecase = AccountDepositUseCase(
            user_repository=UserRepository(db.session),
            account_repository=AccountRepository(db.session),
            transaction_repository=TransactionRepository(db.session),
        )
        return account_usecase(account=account_deposit)


class AccountWithdrawResource(Resource):
    @jwt_required()
    def post(self):
        try:
            adapter = AccountOperationsRequestAdapter()
            data = adapter.load(request.json)
        except ValidationError as e:
            return {"message": str(e)}, 400

        current_user = get_jwt_identity()
        value = data.get("value", None)
        account = data.get("account", None)

        account_deposit = AccountDeposit(value=value, account=account)

        account_usecase = AccountWithdrawUseCase(
            user_repository=UserRepository(db.session),
            account_repository=AccountRepository(db.session),
            transaction_repository=TransactionRepository(db.session),
        )
        return account_usecase(
            account=account_deposit, user_id=current_user.get("id")
        )


class GetTransactionsByAccountResource(Resource):
    @jwt_required()
    def get(self, account_id: int):
        current_user = get_jwt_identity()
        transactions_usecase = AccountTransactionsUseCase(
            transaction_repository=TransactionRepository(db.session),
        )
        return transactions_usecase(
            account_id=account_id, user_id=current_user.get("id")
        )
