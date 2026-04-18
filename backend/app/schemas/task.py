from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import date


# TODO: Define a Priority enum with three values: low, medium, high
# Hint: Look up Python's Enum class — it lets you define a fixed set of allowed values
# Hint: Read the docs — https://docs.python.org/3/library/enum.html
class Priority(str, Enum):
    # Your implementation goes here
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# TODO: Define a Status enum with values: pending, in_progress, completed
class Status(str, Enum):
    # Your implementation goes here
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# TODO: Define the TaskCreate model — what the client sends when creating a task
# Required fields: title (str)
# Optional fields: description, priority, due_date
# Hint: Use Optional[str] for optional string fields
# Hint: Field(...) marks a field as required and lets you add validation constraints
# Hint: Read — https://docs.pydantic.dev/latest/concepts/fields/
class TaskCreate(BaseModel):
    # Your implementation goes here
    title: str = Field(..., description='Title of the task')
    description: str | None = Field(None, description='Optional description of the task')
    priority: Priority | None = Field(Priority.LOW, description='Task priority')
    due_date: date | None = Field(None, description='Due date for the task')


# TODO: Define the TaskUpdate model — all fields optional, client sends only what changes
# Hint: Every single field should be Optional with a default of None
class TaskUpdate(BaseModel):
    # Your implementation goes here
    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    priority: Priority | None = None
    status: Status | None = None


# TODO: Define the TaskResponse model — what we send back to the client
# Should include everything in TaskCreate PLUS: id (int), status (Status)
# Hint: Think about what the server assigns vs what the client provides
class TaskResponse(BaseModel):
    # Your implementation goes here
    id: int
    title: str
    description: str | None = None
    priority: Priority = Priority.LOW
    due_date: date | None = None
    status: Status = Status.PENDING
    # TODO: Add model config to allow reading from ORM objects later
    # Hint: Search for "Pydantic model_config from_attributes"
    model_config = ConfigDict(from_attributes=True)