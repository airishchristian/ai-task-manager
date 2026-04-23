# app/api/routes/ai.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ...dependencies.auth import get_current_active_user
from ...services.ai_service import generate_subtasks

router = APIRouter()

# TODO: Define a request schema (Pydantic model)
# What does the client need to send? Just the task title.
class TaskBreakdownRequest(BaseModel):
    task_title: str

# TODO: Define a response schema
# What do we send back? The original title + list of subtasks
class TaskBreakdownResponse(BaseModel):
    task_title: str
    subtasks: list[str]

# TODO: Create the endpoint
# - Method: POST
# - Path: "/breakdown"
# - Auth: protect with get_current_active_user
# - Call generate_subtasks(request.task_title)
# - Return a TaskBreakdownResponse
@router.post("/", response_model=TaskBreakdownResponse)
def breakdown_task(
    request: TaskBreakdownRequest,
    current_user = Depends(get_current_active_user)
):
    task = generate_subtasks(request.task_title)
    response = TaskBreakdownResponse(task_title=request.task_title, subtasks=task) 
    return response