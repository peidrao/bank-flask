from dataclasses import dataclass
from datetime import date


@dataclass
class Account:
    id: int = None
    user_id: int = None
    amount: float = None
    daily_withdrawal_limit: float = None
    is_active: bool = None
    account_type: int = None
    created_at: date = None


@dataclass
class AccountDeposit:
    account: int = None
    value: float = None
