from flask import Blueprint
from flask_restful import Api

from src.apps.api import resources


def register_resource(blueprint, resource, routes):
    api_blueprint = Blueprint(blueprint, __name__, url_prefix=f"/api/v1/{blueprint}")
    api_v1 = Api(api_blueprint)

    for route in routes:
        url, endpoint = route
        api_v1.add_resource(resource, url, endpoint=endpoint)

    return api_blueprint


auth_blueprint = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
auth_v1 = Api(auth_blueprint)
auth_v1.add_resource(resources.AuthResource, "/token")

user_blueprint = Blueprint("users", __name__, url_prefix="/api/v1/users")
user_v1 = Api(user_blueprint)
user_v1.add_resource(resources.UserResource, "/")
user_v1.add_resource(resources.UserMeResource, "/me")
user_v1.add_resource(resources.PersonDashboardResource, "/dashboard")

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