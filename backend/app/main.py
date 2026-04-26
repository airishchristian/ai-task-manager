from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import tasks
from app.api.routes import auth
from app.api.routes import ai
from app.database import create_db_and_tables
from app.api.routes import summaries

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

app.include_router(auth.router,
                   prefix='/auth',
                   tags=["auth"])

app.include_router(ai.router,
                   prefix='/ai',
                   tags=["ai"])

app.include_router(summaries.router,
                   prefix='/summaries',
                   tags=["summaries"])

@app.get('/')
def root():
    return {"message": "Welcome to Root Page"}

@app.get('/health')
def health_check():
    return {
        "status": "ok",
        "message": 'AI-powered Task Manager'
    }
