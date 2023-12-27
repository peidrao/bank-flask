from marshmallow import ValidationError
from typing import Optional
from werkzeug.security import check_password_hash

from src.infrastructure.database import UserTable
from src.domain.entities import User


class UserRepository:
    def __init__(self, session=None):
        self.session = session

    def create(self, person: User) -> User:
        person_db = UserTable.query.filter_by(email=person.email).first()
        if person_db:
            raise ValidationError("Pessoa já cadastrado")

        person_db = UserTable(
            email=person.email,
            full_name=person.name,
            cpf=person.cpf,
        )
        person_db.set_password(person.password)
        self.session.add(person_db)
        self.session.commit()
        person.id = person_db.id
        return person

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
        person = UserTable.query.filter_by(email=email).first()
        if not person:
            return None
        person = User(
            full_name=person.full_name,
            email=person.email,
            cpf=person.cpf,
            id=person.id,
            password=person.password,
        )
        return person

    def login(self, email: str, password: str) -> User:
        person = self.get_by_email(email)

        if not person:
            return None

        if check_password_hash(person.password, password):
            return person

        return None
