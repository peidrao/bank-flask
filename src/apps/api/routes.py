from flask import Blueprint
from flask_restful import Api

from src.apps.api import resources

auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
auth_v1 = Api(auth_blueprint)
auth_v1.add_resource(resources.AuthResource, "/token")

person_blueprint = Blueprint("person", __name__, url_prefix="/api/v1/person")
person_v1 = Api(person_blueprint)
person_v1.add_resource(resources.PersonResource, "/")
person_v1.add_resource(resources.PersonDashboardResource, "/dashboard")

account_blueprint = Blueprint("account", __name__, url_prefix="/api/v1/account")
account_v1 = Api(account_blueprint)
account_v1.add_resource(resources.AccountResource, "/")
account_v1.add_resource(resources.AccountsMeResource, "/me")
account_v1.add_resource(resources.AccountDetailResource, "/<int:account_id>")
account_v1.add_resource(
    resources.GetTransactionsByAccountResource, "/<int:account_id>/transactions"
)
account_v1.add_resource(resources.AccountDepositResource, "/deposit")
account_v1.add_resource(resources.AccountWithdrawResource, "/withdraw")

transaction_blueprint = Blueprint(
    "transactions", __name__, url_prefix="/api/v1/transactions"
)
transaction_v1 = Api(transaction_blueprint)
transaction_v1.add_resource(resources.GetLastWithdrawsResource, "/withdraws")
