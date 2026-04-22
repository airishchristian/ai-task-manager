from typing import Generator
from sqlmodel import Session
from app.database import engine


def get_db() -> Generator:
    # TODO: Create a Session using the engine
    # TODO: Use try/yield/finally pattern
    # Hint: yield the session, then close it in finally
    # WHY finally? It runs even if an exception is thrown
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()