import pytest
from src.domain.entities.user import User
from src.domain.exceptions import RepositoryErrorException



def test_create_creates_person_successfully(user_repository):
    user = User(
        full_name="John Doe",
        email="johndoe@example.com",
        cpf="12345678901",
        password="test1",
    )
    created_person = user_repository.create(user)

    assert created_person.id is not None
    assert created_person.full_name == "John Doe"
    assert created_person.email == "johndoe@example.com"


def test_create_raises_validation_error_if_email_already_exists(user_repository):
    person1 = User(
        full_name="Alice", email="alice@example.com", cpf="11111111111", password="oi"
    )
    user_repository.create(person1)

    person2 = User(
        full_name="Bob", email="alice@example.com", cpf="22222222222", password="oisas"
    )

    with pytest.raises(RepositoryErrorException):
        user_repository.create(person2)


def test_get_returns_person_by_id(user_repository, user):
    retrieved_person = user_repository.get(user.id)

    assert retrieved_person.id == user.id


def test_get_returns_none_when_person_not_found(user_repository):
    retrieved_person = user_repository.get(123)

    assert retrieved_person is None


def test_get_does_not_include_password(user_repository, user):
    retrieved_person = user_repository.get(user.id)

    assert hasattr(retrieved_person, "password")


def test_get_by_email_returns_person_by_email(user_repository, user):
    retrieved_person = user_repository.get_by_email(user.email)

    assert retrieved_person.id == user.id


def test_get_by_email_returns_none_when_email_not_found(user_repository):
    retrieved_person = user_repository.get_by_email("unknown@example.com")

    assert retrieved_person is None


def test_login_succeeds_with_correct_credentials(user_repository, user):
    logged_in_person = user_repository.login(user.email, "test12345")
    assert logged_in_person.id == user.id
