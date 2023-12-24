from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    id: int = None
    name: str = None
    email: str = None
    password: str = None
    cpf: str = None
    birth_date: date = None
    account: "Account" = None
