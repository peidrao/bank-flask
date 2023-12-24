from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from src.domain.exceptions import PersonNotFoundError
from src.domain.entities import AuthRequest, AuthResponse
from src.infrastructure.repositories import UserRepository


class AuthenticationUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def __call__(self, request: AuthRequest) -> AuthResponse:
        response = AuthResponse(None)
        try:
            email = request.email
            password = request.password

            api_user = self.repository.login(email=email, password=password)

            if not api_user:
                raise PersonNotFoundError(
                    title="Credênciais estão incorretas", code=400
                )
            else:
                api_user.__dict__.pop("password", None)

                access_token = create_access_token(api_user.__dict__)
                refresh_token = create_refresh_token(api_user.__dict__)
                response = AuthResponse(
                    access_token=access_token, refresh_token=refresh_token
                )
        except PersonNotFoundError as e:
            response = jsonify({"error": e.to_dict})
            response.status_code = 400
            return response

        return jsonify(response)
