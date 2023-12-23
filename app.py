from flask import Flask

from config.settings import DEBUG
from src.ext import configuration


if DEBUG:
    import logging
    import warnings

    from http.client import HTTPConnection

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from flask_marshmallow import Marshmallow

    logging.basicConfig(level="DEBUG")
    log = logging.getLogger("urllib3")
    log.setLevel(logging.DEBUG)
    HTTPConnection.debuglevel = 0


def minimal_app():
    app = Flask(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    configuration.init_app(app)
    return app


def create_app():
    app = minimal_app()
    configuration.load_extensions(app)

    @app.shell_context_processor
    def _make_context():
        from src.ext import database

        return dict(app=app, db=database.db)

    return app