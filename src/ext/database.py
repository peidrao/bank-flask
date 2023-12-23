from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(
    session_options={"autoflush": True, "autocommit": False, "expire_on_commit": False},
)


def init_app(app):
    """Initialize models"""
    from src.infrastructure.database import (  # noqa: F401
        AccountTable,
        PersonTable,
        TransactionTable,
    )

    """Initialize database"""
    db.init_app(app)
