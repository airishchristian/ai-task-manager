from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ...dependencies.database import get_db
from ...dependencies.auth import get_current_active_user
from ...models.task import Task
from ...schemas.task import TaskCreate, TaskResponse, TaskUpdate, Status

router = APIRouter()


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
    status: Status | None = None, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    GET /tasks?status=pending&current_user=1

    TODO:
    - Start with statement = select(Task)
    - If status is provided, add .where(Task.status == status)
    - If current_user is provided, add .where(Task.current_user == current_user)
    - Hint: you can chain .where() calls
    - Return session.exec(statement).all()
    """
    statement = select(Task)
    if status is not None:
        statement = statement.where(Task.status == status).where(Task.user_id == current_user.id)
    result = db.exec(statement).all()
    return result

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    GET /tasks/{task_id}

    TODO:
    - Open a Session
    - Use session.get(Task, task_id) to find the task
    - If task is None, raise HTTPException 404
    - Otherwise return the task
    """
    # Your implementation goes here
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Item not found')
    return task

@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)

):
    """
    POST /tasks

    TODO:
    - Create a Task object from task_data
      Hint: Task(**task_data.model_dump())
    - Add it, commit, refresh, return it
    """
    # Your implementation goes here
    task_data = Task(**task.model_dump())
    db.add(task_data)
    db.commit()
    db.refresh(task_data)
    return task_data


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, 
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
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
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')
    update_data = task_update.model_dump(exclude_unset=True)
    task.sqlmodel_update(update_data)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """  
    DELETE /tasks/{task_id}

    TODO:
    - Open a Session
    - Find the task (raise 404 if not found)
    - Delete it, commit, return None
    """
    # Your implementation goes here
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None