import requests
from app import create_app
from config import Config

app = create_app()


@app.cli.group()
def manage():
    pass


@manage.command()
def createbanks():
    from src.ext.database import db
    from src.infrastructure.repositories import BankRepository
    from src.infrastructure.database import BankTable

    bank_repository = BankRepository(db.session)
    response = requests.get(Config)

    if response.status_code == 200:
        banks_list = response.json()["payload"]["blob"]["csv"][1:51]
        for b in banks_list:
            if not bank_repository.get(compe=b[0]):
                bank = BankTable(
                    compe=b[0],
                    ispb=b[1],
                    document=b[2],
                    long_name=b[3],
                    short_name=b[4],
                )
                db.session.add(bank)

        db.session.commit()


if __name__ == "__main__":
    manage()
