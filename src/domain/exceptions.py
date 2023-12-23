from src.ext.errors import Error


class PersonNotFoundError(Error):
    def __str__(self):
        return "Pessoa não encontrada."
