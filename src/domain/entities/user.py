from dataclasses import dataclass


@dataclass
class User:
    id: int = None
    full_name: str = None
    email: str = None
    password: str = None
    cpf: str = None
    account: "Account" = None
