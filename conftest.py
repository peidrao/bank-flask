import pytest
from flask import Flask
from flask_jwt_extended import create_access_token

from src.blueprints import api_v1
from src.domain.entities.account import Account
from src.ext import database, token
from src.infrastructure.database.person import PersonTable
from src.infrastructure.repositories.account import AccountRepository
from src.infrastructure.repositories.person import PersonRepository
from src.infrastructure.repositories.transaction import TransactionRepository


@pytest.fixture(scope="session")
def app(fake):
    app_test = Flask(__name__, instance_relative_config=True)
    app_test.url_map.strict_slashes = False
    app_test.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app_test.config["SQLALCHEMY_BINDS"] = {"admin": "sqlite://"}
    app_test.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app_test.config["JWT_SECRET_KEY"] = fake.pystr()

    api_v1.init_app(app_test)
    token.init_test_app(app_test)
    database.init_app(app_test)
    return app_test


@pytest.fixture
def db(app):
    from src.ext.database import db as _db

    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope="session")
def fake():
    from faker import Faker

    return Faker("pt_BR")


@pytest.fixture
def authenticated_header():
    access_token = create_access_token({})
    return {"Authorization": "Bearer {}".format(access_token)}


@pytest.fixture
def person(db, fake) -> PersonRepository:
    person_data = {
        "email": fake.email(),
        "password": "test12345",
        "name": fake.name(),
        "cpf": fake.cpf(),
        "birth_date": fake.date_of_birth(),
    }
    person = PersonTable(**person_data)
    person.set_password("test12345")

    db.session.add(person)
    db.session.commit()

    return person


@pytest.fixture
def transaction_repository(db) -> TransactionRepository:
    return TransactionRepository(session=db.session)


@pytest.fixture
def account_repository(db) -> AccountRepository:
    return AccountRepository(session=db.session)


@pytest.fixture
def create_account(account_repository: AccountRepository):
    def _create_account(**kwargs) -> Account:
        account = Account(**kwargs)
        account_repository.create(account)
        return account

    return _create_account


@pytest.fixture
def person_repository(db) -> PersonRepository:
    return PersonRepository(session=db.session)
