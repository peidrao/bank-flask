from flask import jsonify
from src.infrastructure.repositories.transaction import TransactionRepository


class GetLastWithdrawsUseCase:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
    ):
        self.transaction_repository = transaction_repository

    def __call__(
        self,
        person_id: int,
        limit: int,
    ):
        transactions_db = self.transaction_repository.get_last_transactions(
            person_id=person_id, limit=limit
        )

        if not transactions_db:
            return []

        return jsonify(transactions_db)
