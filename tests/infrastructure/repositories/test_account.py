from src.domain.entities.account import Account
from src.infrastructure.database.account import AccountTable


def test_create_account(account_repository, person):
    account_data = {
        "user_id": person.id,
        "daily_withdrawal_limit": 500.0,
    }
    account = Account(**account_data)

    created_account = account_repository.create(account)

    assert created_account.id is not None
    assert created_account.user_id == account_data["user_id"]
    assert (
        created_account.daily_withdrawal_limit == account_data["daily_withdrawal_limit"]
    )


def test_create_account_commit(db, account_repository, person):
    account_data = {
        "user_id": person.id,
        "daily_withdrawal_limit": 500.0,
    }
    account = Account(**account_data)

    created_account = account_repository.create(account)

    db.session.commit()
    with db.session.no_autoflush:
        retrieved_account = db.session.get(AccountTable, created_account.id)
        assert retrieved_account is not None


def test_get_by_person_id_returns_account_when_found(
    account_repository, create_account, person
):
    created_account = create_account(user_id=person.id)

    retrieved_account = account_repository.get_by_user_id(
        user_id=person.id,
    )

    assert retrieved_account.id == created_account.id


def test_get_by_person_id_returns_none_when_not_found(account_repository):
    user_id = 456

    retrieved_account = account_repository.get_by_user_id(user_id)

    assert retrieved_account is None


def test_get_by_args_returns_account_when_found(
    account_repository, create_account, person
):
    account = create_account(user_id=person.id)

    retrieved_account = account_repository.get_by_args(user_id=person.id)

    assert retrieved_account.id == account.id


def test_get_by_args_returns_none_when_not_found(account_repository):
    retrieved_account = account_repository.get_by_args(user_id=10)
    assert retrieved_account is None


def test_get_accounts_info_returns_correct_total_and_count(
    account_repository, create_account, person
):
    create_account(amount=100, user_id=person.id)

    create_account(amount=200, user_id=person.id)

    total_amount, account_count = account_repository.get_accounts_info(
        user_id=person.id
    )

    assert total_amount == 0
    assert account_count == 2


def test_get_accounts_info_returns_zero_when_no_accounts_found(account_repository):
    total_amount, account_count = account_repository.get_accounts_info(456)

    assert total_amount == 0
    assert account_count == 0


def test_filter_returns_accounts_matching_criteria(
    account_repository, create_account, person
):
    create_account(user_id=person.id)
    create_account(user_id=person.id)
    create_account(user_id=person.id)

    filtered_accounts = account_repository.filter(user_id=person.id)

    assert len(filtered_accounts) == 3


def test_filter_returns_empty_list_when_no_accounts_match(account_repository):
    filtered_accounts = account_repository.filter()

    assert filtered_accounts == []


def test_update_account_updates_fields_correctly(
    account_repository, create_account, person
):
    account = create_account(user_id=person.id)

    updated_account = account_repository.update_account(
        account.id, daily_withdrawal_limit=500
    )

    assert updated_account.daily_withdrawal_limit == 500


def test_update_account_returns_none_when_account_not_found(account_repository):
    updated_account = account_repository.update_account(123, amount=500)

    assert updated_account is None
