from flask_jwt_extended import JWTManager


def init_app(app):
    _ = JWTManager(app)


def init_test_app(app):
    _ = JWTManager(app)
