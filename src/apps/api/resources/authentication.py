from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src.infrastructure.repositories import UserRepository
from src.apps.api.adapters import AuthRequestAdapter
from src.domain.entities import AuthRequest
from src.apps.usecases import AuthenticationUseCase

from src.ext.database import db


class AuthResource(Resource):
    def post(self):
        try:
            adapter = AuthRequestAdapter()
            data = adapter.load(request.json)
        except ValidationError as e:
            return {"message": str(e)}, 400

        email = data.get("email", None)
        password = data.get("password", None)

        request_model = AuthRequest(email, password)

        auth = AuthenticationUseCase(repository=UserRepository(db.session))
        return auth(request_model)
