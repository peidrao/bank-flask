from datetime import date
from src.infrastructure.database.transaction import TransactionTable
from src.domain.entities import Transaction


def test_create_transaction(transaction_repository):
    transaction_data = {
        "account_id": 1,
        "value": 100.0,
        "type": "credit",
    }
    transaction = Transaction(**transaction_data)

    created_transaction = transaction_repository.create(transaction)

    assert created_transaction.id is not None
    assert created_transaction.account_id == transaction_data["account_id"]
    assert created_transaction.value == transaction_data["value"]
    assert created_transaction.type == transaction_data["type"]


def test_get_aggregate_value_in_one_day(transaction_repository):
    account_id = 1
    today = date.today()
    transactions_data = [
        {
            "value": 50.0,
            "type": "-",
            "account_id": account_id,
            "created_at": today,
        },
        {
            "value": 30.0,
            "type": "-",
            "account_id": account_id,
            "created_at": today,
        },
        {
            "value": 20.0,
            "type": "+",
            "account_id": account_id,
            "created_at": today,
        },
    ]

    for data in transactions_data:
        transaction = TransactionTable(**data)
        transaction_repository.session.add(transaction)

    transaction_repository.session.commit()

    total_value = transaction_repository.get_aggregate_value_in_one_day(account_id)

    assert total_value == 80.0


def test_get_aggregate_value_in_one_day_no_transactions(transaction_repository):
    account_id = 2
    total_value = transaction_repository.get_aggregate_value_in_one_day(account_id)

    assert total_value == 0.0


def test_filter_transactions_by_person_no_transactions(transaction_repository, person):
    (
        transactions,
        cash_in,
        cash_out,
    ) = transaction_repository.filter_transactions_by_person(user_id=person.id)

    assert transactions is None
    assert cash_in == 0
    assert cash_out == 0
