from flask_marshmallow import Schema
from marshmallow import EXCLUDE, fields


class AutenticacaoAdapter(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    email = fields.Email(data_key="email", required=True, load_only=True)
    senha = fields.Str(data_key="password", required=True, load_only=True)
    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)


class AuthRequestAdapter(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserRequestAdapter(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    full_name = fields.Str(required=True)
    cpf = fields.Str(required=True)


class AuthAdapter(Schema):
    access_token = fields.Method(
        serialize="serialize_access_token", data_key="access_token"
    )
    refresh_token = fields.Method(
        serialize="serialize_refresh_token", data_key="refresh_token"
    )

    @staticmethod
    def serialize_access_token(obj):
        return obj["access_token"]

    @staticmethod
    def serialize_refresh_token(obj):
        return obj["refresh_token"]
