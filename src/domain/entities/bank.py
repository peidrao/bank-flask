from dataclasses import dataclass


@dataclass
class Bank:
    id: int = None
    compe: str = None
    ispb: str = None
    document: str = None
    long_name: str = None
    short_name: str = None
