from flask_marshmallow import Marshmallow


def init_app(app):
    marshmallow = Marshmallow()
    marshmallow.init_app(app)
