from src.apps.api import resources

API_PREFIX = "/api/v1"
BLUEPRINTS = [
    ("auth", "/auth", [(resources.AuthResource, "/token")]),
    (
        "users",
        "/users",
        [
            (resources.UserResource, "/"),
            (resources.UserMeResource, "/me"),
            (resources.UserDashboardResource, "/dashboard"),
        ],
    ),
    (
        "account",
        "/accounts",
        [
            (resources.AccountResource, "/"),
            (resources.AccountsMeResource, "/me"),
            (resources.AccountDetailResource, "/<int:account_id>"),
            (
                resources.GetTransactionsByAccountResource,
                "/<int:account_id>/transactions",
            ),
            (resources.AccountDepositResource, "/deposit"),
            (resources.AccountWithdrawResource, "/withdraw"),
        ],
    ),
    ("transactions", "/transactions", [
        (resources.GetLastWithdrawsResource, "/withdraws")
    ]),

]
