from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request
from flask_restful import Resource

from src.apps.usecases import GetLastWithdrawsUseCase
from src.infrastructure.repositories.transaction import TransactionRepository
from src.ext.database import db


class GetLastWithdrawsResource(Resource):
    @jwt_required()
    def get(self):
        limit = int(request.args.get("limit", 0))
        current_person = get_jwt_identity()
        withdraws_usecase = GetLastWithdrawsUseCase(
            transaction_repository=TransactionRepository(db.session),
        )
        return withdraws_usecase(limit=limit, person_id=current_person.get("id"))
