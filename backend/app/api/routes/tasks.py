from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from ...schemas.task import TaskCreate, TaskResponse, TaskUpdate, Status, Priority
from ...database import engine
from ...models.task import Task
from ...core.security import verify_token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
# Temporary in-memory storage (replaces database for now)
# Think of this as your fake database — just a Python list
# fake_tasks_db = [
#     {"id": 1, "title": "Learn FastAPI", "description":None, "priority":Priority.LOW, "due_date":None, "status": Status.PENDING},
#     {"id": 2, "title": "Build task manager", "description":None, "priority":Priority.LOW, "due_date":None, "status": Status.IN_PROGRESS},
#     {"id": 3, "title": "Deploy to Render", "description":None, "priority":Priority.LOW, "due_date":None, "status": Status.PENDING},
# ]

def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
    """
    TODO:
    - Call verify_token(token)
    - If the result is None → raise HTTPException 401
      with detail="Invalid or expired token"
      and headers={"WWW-Authenticate": "Bearer"}
    - Return the email string
    """
    # Your implementation goes here
    verified = verify_token(token)
    if not verified:
        raise HTTPException(status_code=401, 
                            detail="Invalid or expired token",
                            headers={"WWW-Authenticate": "Bearer"}
        )
    return verified

@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(status: Status | None = None, 
                  current_user: str = Depends(get_current_user_email)
):
    """
    GET /tasks?status=pending&current_user=1

    TODO:
    - Open a Session
    - Start with statement = select(Task)
    - If status is provided, add .where(Task.status == status)
    - If current_user is provided, add .where(Task.current_user == current_user)
    - Hint: you can chain .where() calls
    - Return session.exec(statement).all()
    """
    with Session(engine) as session:
        statement = select(Task)
        if status is not None:
            statement = statement.where(Task.status == status)
        result = session.exec(statement).all()
        return result

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int):
    """
    GET /tasks/{task_id}

    TODO:
    - Open a Session
    - Use session.get(Task, task_id) to find the task
    - If task is None, raise HTTPException 404
    - Otherwise return the task
    """
    # Your implementation goes here
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail='Item not found')
        return task

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """
    POST /tasks

    TODO:
    - Open a Session
    - Create a Task object from task_data
      Hint: Task(**task_data.model_dump())
    - Add it, commit, refresh, return it
    """
    # Your implementation goes here
    with Session(engine) as session:
        task_data = Task(**task.model_dump())
        session.add(task_data)
        session.commit()
        session.refresh(task_data)
        return task_data


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate):
    """
    PATCH /tasks/{task_id}
    Updates only the fields that were sent.

    TODO:
    - Open a Session
    - Find the task (raise 404 if not found)
    - Get only the fields that were actually sent:
        update_task = task_update.model_dump(exclude_unset=True)
    - Loop through update_data and use setattr() to apply each change
    - Add, commit, refresh, return
    """
    # Your implementation goes here
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')
        update_data = task_update.model_dump(exclude_unset=True)
        task.sqlmodel_update(update_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int):
    """
    DELETE /tasks/{task_id}

    TODO:
    - Open a Session
    - Find the task (raise 404 if not found)
    - Delete it, commit, return None
    """
    # Your implementation goes here
    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
        return None