from dataclasses import dataclass


@dataclass
class User:
    id: int = None
    full_name: str = None
    email: str = None
    password: str = None
    is_superuser: bool = None
    cpf: str = None
    account: "Account" = None
