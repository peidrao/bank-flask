from typing import Optional
from werkzeug.security import check_password_hash

from src.infrastructure.database import UserTable
from src.domain.entities import User
from src.domain.exceptions import RepositoryErrorException


class UserRepository:
    def __init__(self, session=None):
        self.session = session

    def create(self, user: User) -> User:
        user_db = UserTable.query.filter_by(email=user.email).first()
        if user_db:
            raise RepositoryErrorException(
                "Já existe um usuário com esse e-mail", status_code=400
            )
        new_user = UserTable(
            email=user.email,
            full_name=user.full_name,
            cpf=user.cpf,
            is_superuser=user.is_superuser,
        )
        new_user.set_password(user.password)
        self.session.add(new_user)
        self.session.commit()
        user.id = new_user.id
        return user

    def get(self, id: int) -> Optional[User]:
        user = UserTable.query.filter_by(id=id).first()
        if not user:
            return None
        user = User(
            full_name=user.full_name,
            email=user.email,
            cpf=user.cpf,
            id=user.id,
        )
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        user = UserTable.query.filter_by(email=email).first()
        if not user:
            return None
        user = User(
            full_name=user.full_name,
            email=user.email,
            cpf=user.cpf,
            id=user.id,
            password=user.password,
        )
        return user

    def login(self, email: str, password: str) -> User:
        user = self.get_by_email(email)

        if not user:
            return None
        
        if check_password_hash(user.password, password):
            return user

        return None
