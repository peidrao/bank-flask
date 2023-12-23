from marshmallow import ValidationError
from typing import Optional
from werkzeug.security import check_password_hash

from src.infrastructure.database import PersonTable
from src.domain.entities import Person


class PersonRepository:
    def __init__(self, session=None):
        self.session = session

    def create(self, person: Person) -> Person:
        person_db = PersonTable.query.filter_by(email=person.email).first()
        if person_db:
            raise ValidationError("Pessoa já cadastrado")
        person_db = PersonTable(
            email=person.email,
            name=person.name,
            cpf=person.cpf,
            birth_date=person.birth_date,
        )
        person_db.set_password(person.password)
        self.session.add(person_db)
        self.session.commit()
        person.id = person_db.id
        return person

    def get(self, id: int) -> Optional[Person]:
        person = PersonTable.query.filter_by(id=id).first()
        if not person:
            return None
        person = Person(
            name=person.name,
            email=person.email,
            cpf=person.cpf,
            id=person.id,
            birth_date=person.birth_date,
        )
        return person

    def get_by_email(self, email: str) -> Optional[Person]:
        person = PersonTable.query.filter_by(email=email).first()
        if not person:
            return None
        person = Person(
            name=person.name,
            email=person.email,
            cpf=person.cpf,
            id=person.id,
            birth_date=person.birth_date,
            password=person.password,
        )
        return person

    def login(self, email: str, password: str) -> Person:
        person = self.get_by_email(email)

        if not person:
            return None

        if check_password_hash(person.password, password):
            return person

        return None
