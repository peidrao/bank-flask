from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from src.infrastructure.repositories import (
    UserRepository,
    AccountRepository,
    TransactionRepository,
)
from src.apps.api.adapters import UserRequestAdapter
from src.domain.entities import User
from src.apps.usecases import (
    CreatePersonUseCase,
    PersonMeUseCase,
    PersonDashboardUseCase,
)

from src.ext.database import db


class UserResource(Resource):
    def post(self):
        try:
            adapter = UserRequestAdapter()
            data = adapter.load(request.json)
        except ValidationError as e:
            return {"message": str(e)}, 400

        email = data.get("email", None)
        name = data.get("full_name", None)
        password = data.get("password", None)
        cpf = data.get("cpf", None)
        request_person = User(
            email=email,
            password=password,
            full_name=name,
            cpf=cpf,
        )

        person = CreatePersonUseCase(
            person_repository=UserRepository(db.session),
            account_repository=AccountRepository(db.session),
        )
        return person(request_person)

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        person = PersonMeUseCase(
            person_repository=UserRepository(db.session),
            account_repository=AccountRepository(db.session),
        )

        return person(person_id=current_user.get("id"))


class PersonDashboardResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        person_dashboard = PersonDashboardUseCase(
            transaction_repository=TransactionRepository(db.session),
            account_repository=AccountRepository(db.session),
        )

        return person_dashboard(person_id=current_user.get("id"))
