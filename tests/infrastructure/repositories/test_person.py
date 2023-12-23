from marshmallow import ValidationError
import pytest
from src.domain.entities.person import Person


def test_create_creates_person_successfully(person_repository):
    person = Person(
        name="John Doe",
        email="johndoe@example.com",
        cpf="12345678901",
        password="test1",
    )
    created_person = person_repository.create(person)

    assert created_person.id is not None
    assert created_person.name == "John Doe"
    assert created_person.email == "johndoe@example.com"


def test_create_raises_validation_error_if_email_already_exists(person_repository):
    person1 = Person(
        name="Alice", email="alice@example.com", cpf="11111111111", password="oi"
    )
    person_repository.create(person1)

    person2 = Person(
        name="Bob", email="alice@example.com", cpf="22222222222", password="oisas"
    )

    with pytest.raises(ValidationError):
        person_repository.create(person2)


def test_get_returns_person_by_id(person_repository, person):
    retrieved_person = person_repository.get(person.id)

    assert retrieved_person.id == person.id


def test_get_returns_none_when_person_not_found(person_repository):
    retrieved_person = person_repository.get(123)

    assert retrieved_person is None


def test_get_does_not_include_password(person_repository, person):
    retrieved_person = person_repository.get(person.id)

    assert hasattr(retrieved_person, "password")


def test_get_by_email_returns_person_by_email(person_repository, person):
    retrieved_person = person_repository.get_by_email(person.email)

    assert retrieved_person.id == person.id


def test_get_by_email_returns_none_when_email_not_found(person_repository):
    retrieved_person = person_repository.get_by_email("unknown@example.com")

    assert retrieved_person is None


def test_login_succeeds_with_correct_credentials(person_repository, person):
    logged_in_person = person_repository.login(person.email, "test12345")
    assert logged_in_person.id == person.id
