from fastapi import FastAPI
from .routers import tasks

app = FastAPI(
    title='AI Task Manager',
    description='An AI-powered Task Manager app built with FastAPI',
    version='1.0.0'
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
