# app/database.py
from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Import BOTH models here
# WHY: SQLModel must "see" every model before create_all runs
# from .models.task import Task
# from .models.??? import ???
from .models.task import Task
from .models.user import User


# TODO: Define the SQLite database URL
# Format: "sqlite:///./filename.db"
# The file will appear in your backend/ folder when the server runs
sqlite_url = os.environ.get('DATABASE_URL')

# TODO: Create the engine
# echo=True prints every SQL query to your terminal — great for learning
engine = create_engine(sqlite_url, echo=True)


# TODO: Implement this function
# Hint: SQLModel.metadata.create_all(engine)
def create_db_and_tables():
    # your implementation
    SQLModel.metadata.create_all(engine)