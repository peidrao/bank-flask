from dataclasses import dataclass


@dataclass
class AuthRequest:
    email: str = None
    password: str = None


@dataclass
class AuthResponse:
    access_token: str = None
    refresh_token: str = None
