from fastapi import APIRouter, HTTPException

router = APIRouter()

# Temporary in-memory storage (replaces database for now)
# Think of this as your fake database — just a Python list
fake_tasks_db = [
    {"id": 1, "title": "Learn FastAPI", "status": "pending"},
    {"id": 2, "title": "Build task manager", "status": "in_progress"},
    {"id": 3, "title": "Deploy to Render", "status": "pending"},
]


@router.get("/", status_code=200)
def get_all_tasks(status: str = None):
    """
    GET /tasks
    Returns all tasks.
    If a 'status' query parameter is provided, filter by that status.

    TODO:
    - If status is None, return all tasks
    - If status is provided, return only tasks where task["status"] == status
    - Hint: think about list comprehension or a simple loop + condition
    """
    tasks = []
    if status is None:
        return fake_tasks_db
    for task in fake_tasks_db:
        if task['status'] == status:
            tasks.append(task)
    return tasks

@router.get("/{task_id}", status_code=200)
def get_task_by_id(task_id: int):
    """
    GET /tasks/{task_id}
    Returns a single task by its ID.

    TODO:
    - Loop through fake_tasks_db
    - Find the task where task["id"] == task_id
    - If found, return it
    - If not found, what should you return?
      Hint: look up HTTPException in FastAPI docs
    """
    # Your implementation goes here
    for task in fake_tasks_db:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail='Item not found')


@router.post("/", status_code=201)
def create_task(title: str):
    """
    POST /tasks
    Creates a new task with the given title.

    TODO:
    - Generate a new id (hint: think about the length of fake_tasks_db)
    - Create a new task dict with id, title, and a default status of "pending"
    - Append it to fake_tasks_db
    - Return the newly created task
    """
    # Your implementation goes here
    new_task = {
        "id": len(fake_tasks_db) + 1,
        "title": title,
        "status": "pending", 
    }
    fake_tasks_db.append(new_task)

    return new_task

@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: int):
    """
    DELETE /tasks/{task_id}
    Deletes a task by its ID.

    TODO:
    - Find the task with the matching task_id
    - If not found, raise HTTPException 404
    - If found, remove it from fake_tasks_db
      Hint: look up list.remove() or list comprehension to rebuild the list
    - Return a confirmation message
    """
    # Your implementation goes here
    for num in range(len(fake_tasks_db)):
        if fake_tasks_db[num]['id'] == task_id:
            fake_tasks_db.pop(num)
            return "Deleted Successfully"