from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import tasks
from app.database import create_db_and_tables


# TODO: Implement the lifespan function
# This runs create_db_and_tables at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # your implementation — call create_db_and_tables here
    create_db_and_tables()
    yield 

app = FastAPI(
    title='AI Task Manager',
    description='An AI-powered Task Manager app built with FastAPI',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(tasks.router,
                   prefix='/tasks',
                   tags=['tasks']
                   )

@app.get('/')
def root():
    return {"message": "Welcome to Root Page"}

@app.get('/health')
def health_check():
    return {
        "status": "ok",
        "message": 'AI-powered Task Manager'
    }
