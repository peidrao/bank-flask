from src.apps.api.routes import (
    auth_blueprint,
    person_blueprint,
    account_blueprint,
    transaction_blueprint,
)


def init_app(app):
    """Initialize blueprints"""
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(person_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(transaction_blueprint)
