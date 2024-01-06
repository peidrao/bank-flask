from dataclasses import dataclass
from datetime import date


@dataclass
class Transaction:
    id: int = None
    account_id: int = None
    value: float = None
    type: str = None
    created_at: date = None
