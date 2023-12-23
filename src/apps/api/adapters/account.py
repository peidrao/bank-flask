from flask_marshmallow import Schema
from marshmallow import fields


class AccountOperationsRequestAdapter(Schema):
    account = fields.Int(required=True)
    value = fields.Float(required=True)


class AccountRequestAdapter(Schema):
    daily_withdrawal_limit = fields.Float(required=False, allow_none=True)
    account_type = fields.Int(required=False, allow_none=True)
    is_active = fields.Bool(required=False, allow_none=True)
