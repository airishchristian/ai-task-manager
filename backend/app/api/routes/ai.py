# app/api/routes/ai.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import date
from ...dependencies.auth import get_current_active_user
from ...services.ai_service import generate_subtasks, suggest_priority

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
@router.post("/breakdown", response_model=TaskBreakdownResponse)
def breakdown_task(
    request: TaskBreakdownRequest,
    current_user = Depends(get_current_active_user)
):
    task = generate_subtasks(request.task_title)
    return TaskBreakdownResponse(task_title=request.task_title, subtasks=task) 


# TODO 1: Define PrioritizeRequest
# What three fields does the client send?
# - task_title: required string
# - description: optional string, default None
# - due_date: optional date (use Python's date type), default None
class PrioritizeRequest(BaseModel):
    task_title: str
    description: str | None = None
    due_date: date | None = None

# TODO 2: Define PrioritizeResponse
# What does the client get back?
# - task_title: str
# - priority: str  
# - reasoning: str
class PrioritizeResponse(BaseModel):
    task_title: str
    priority: str
    reasoning: str

# TODO 3: Implement the endpoint
# - POST to "/prioritize"
# - Protected with get_current_active_user
# - Call suggest_priority() — look at its signature: what arguments does it take?
# - One tricky part: suggest_priority() expects due_date as str | None
#   but request.due_date is a date object | None
#   How do you convert a date object to a string? Hint: str() or .isoformat()
# - Return a PrioritizeResponse
@router.post("/prioritize", response_model=PrioritizeResponse)
def prioritize_task(
    request: PrioritizeRequest,
    current_user = Depends(get_current_active_user)
):
    suggestion = suggest_priority(
        task_title=request.task_title, 
        description=request.description, 
        due_date = request.due_date.isoformat() if request.due_date else None
    )
    return PrioritizeResponse(
        task_title=request.task_title, 
        priority=suggestion["priority"],
        reasoning=suggestion["reasoning"]
    )