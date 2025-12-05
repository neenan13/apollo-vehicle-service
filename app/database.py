from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Local SQLite database, keeps the service self-contained for evaluation.


SQLALCHEMY_DATABASE_URL = "sqlite:///./vehicles.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models

Base = declarative_base()


def get_db():

    """
    Creates a request based database session.
    Makes sure taht each request gets its own proper session.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
