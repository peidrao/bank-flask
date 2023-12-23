from app import create_app


app = create_app()


@app.cli.group()
def manage():
    pass


@manage.command()
def createperson():
    from src.ext.database import db
    from src.infrastructure.repositories import PersonRepository
    from src.domain.entities import Person

    person_repository = PersonRepository(db.session)
    try:
        person_repository.create(
            Person(
                name="Elon Musk",
                email="elon@musk.com",
                birth_date="1971-06-28",
                password="123",
            )
        )
        print("Pessoa criada com sucesso!")
    except:
        print("Já existe uma pessoa criada com esse email!")


if __name__ == "__main__":
    manage()
