from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Import your Task model
# WHY: SQLModel must "see" the model before create_all works
# from app.models.??? import ???
from .models.task import Task


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