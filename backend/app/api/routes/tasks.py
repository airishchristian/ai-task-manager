from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ...schemas.task import TaskCreate, TaskResponse, TaskUpdate, Status, Priority
from ...database import engine
from ...models.task import Task


router = APIRouter()

# Temporary in-memory storage (replaces database for now)
# Think of this as your fake database — just a Python list
# fake_tasks_db = [
#     {"id": 1, "title": "Learn FastAPI", "description":None, "priority":Priority.LOW, "due_date":None, "status": Status.PENDING},
#     {"id": 2, "title": "Build task manager", "description":None, "priority":Priority.LOW, "due_date":None, "status": Status.IN_PROGRESS},
#     {"id": 3, "title": "Deploy to Render", "description":None, "priority":Priority.LOW, "due_date":None, "status": Status.PENDING},
# ]


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(status: Status | None = None):
    """
    GET /tasks
    Returns all tasks, optionally filtered by status.

    TODO:
    - Open a Session using: with Session(engine) as session:
    - If status is None, return all tasks using select(Task)
    - If status is provided, add a .where() filter
    - Use session.exec(...).all() to get a list
    """
    with Session(engine) as session:
        if status is None:
            statement = select(Task)
        else:
            statement = select(Task).where(Task.status == status)
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
        
        update_task = task_update.model_dump(exclude_unset=True)
        task.sqlmodel_update(update_task)
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
        return {"message": "Deleted Successfully"}