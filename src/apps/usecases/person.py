from flask import jsonify

from src.infrastructure.repositories import UserRepository, AccountRepository
from src.domain.entities import User, Account
from src.infrastructure.repositories.transaction import TransactionRepository


class CreatePersonUseCase:
    def __init__(
        self,
        person_repository: UserRepository,
        account_repository: AccountRepository,
    ):
        self.person_repository = person_repository
        self.account_repository = account_repository

    def __call__(self, request: User):
        try:
            person = self.person_repository.create(request)
            self.account_repository.create(
                Account(
                    person_id=person.id, account_type=1, daily_withdrawal_limit=200.00
                )
            )
        except:
            return {"erro": "Erro ao criar conta"}, 400

        return {"message": "Conta criada com sucesso!"}, 201


class PersonMeUseCase:
    def __init__(
        self,
        person_repository: UserRepository,
        account_repository: AccountRepository,
    ):
        self.person_repository = person_repository
        self.account_repository = account_repository

    def __call__(self, person_id: int):
        person = self.person_repository.get(person_id)

        if person:
            account = self.account_repository.get_by_person_id(person_id)

        response = User(
            id=person.id,
            name=person.name,
            email=person.email,
            birth_date=person.birth_date,
            cpf=person.cpf,
            account=account,
        )

        return jsonify(response)


class PersonDashboardUseCase:
    def __init__(
        self,
        account_repository: AccountRepository,
        transaction_repository: TransactionRepository,
    ):
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository

    def __call__(
        self,
        person_id: int,
    ):
        (
            transactions_db,
            transactions_cash_in,
            transactions_cash_out,
        ) = self.transaction_repository.filter_transactions_by_person(
            person_id=person_id
        )

        accounts_amount, accounts_total = self.account_repository.get_accounts_info(
            person_id
        )

        transactions = []
        if transactions_db:
            transactions = transactions_db

        response_data = {
            "transactions": transactions,
            "transactions_cash_in": transactions_cash_in,
            "transactions_cash_out": transactions_cash_out,
            "accounts_amount": accounts_amount,
            "accounts_total": accounts_total,
        }

        response = jsonify(response_data)

        return response
