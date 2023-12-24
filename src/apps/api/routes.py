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


auth_routes = [("/token", "AuthResource")]
auth_blueprint = register_resource("auth", resources.AuthResource, auth_routes)

user_routes = [("/", "UserResource"), ("/dashboard", "PersonDashboardResource")]
person_blueprint = register_resource("users", resources.UserResource, user_routes)

account_routes = [
    ("/", "AccountResource"),
    ("/me", "AccountsMeResource"),
    ("/<int:account_id>", "AccountDetailResource"),
    ("/<int:account_id>/transactions", "GetTransactionsByAccountResource"),
    ("/deposit", "AccountDepositResource"),
    ("/withdraw", "AccountWithdrawResource"),
]
account_blueprint = register_resource(
    "account", resources.AccountResource, account_routes
)

# Register Transaction resources
transaction_routes = [("/withdraws", "GetLastWithdrawsResource")]
transaction_blueprint = register_resource(
    "transactions",
    resources.GetLastWithdrawsResource,
    transaction_routes,
)
