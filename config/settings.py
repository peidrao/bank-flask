import os
from datetime import timedelta
from decouple import config

DEBUG = config("FLASK_DEBUG", cast=bool, default=False)

EXTENSIONS = [
    "src.ext.database",
    "src.ext.serializer",
    "src.ext.migration",
    "src.ext.token",
    "src.ext.cors",
    "src.blueprints.api_v1",
]

THIS_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(THIS_PATH))
SECRET_KEY = config("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = config("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = True

JWT_SECRET_KEY = config("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(60)
