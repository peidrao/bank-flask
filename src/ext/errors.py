from dataclasses import dataclass


@dataclass
class Error(Exception):
    code: int = 999
    title: str = "Ocorreu um erro inesperado"
    traceback: any = None

    def __str__(self):
        return self.message

    @property
    def to_dict(self):
        data = self.__dict__.copy()
        data.pop("message", None)
        data.pop("traceback", None)
        return data
