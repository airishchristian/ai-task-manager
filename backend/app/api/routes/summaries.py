# app/api/routes/summaries.py
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select
from ...models.summary import Summary
from ...models.task import Task
from ...services.ai_service import generate_weekly_summary
from ...dependencies.database import get_db
from ...dependencies.auth import get_current_active_user
from ...database import engine  # needed for background task session

router = APIRouter()

def _run_summary_generation(user_id: int, user_name: str):
    """
    This runs IN THE BACKGROUND after the response is sent.
    
    TODO:
    - Create a NEW Session manually (NOT via Depends — why?)
      Hint: with Session(engine) as db:
    - Query ALL tasks where Task.user_id == user_id
    - If no tasks found, return early (nothing to summarize)
    - Convert tasks to a list of dicts
      Hint: [task.model_dump() for task in tasks]
      But model_dump() includes date objects — Claude needs strings
      Hint: convert with: [{**t, "due_date": str(t["due_date"])} for t in raw]
    - Call generate_weekly_summary(tasks_as_dicts, user_name)
    - Create a Summary(content=..., user_id=user_id) object
    - Save it to the database
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        if not tasks:
            return
        raw = [task.model_dump() for task in tasks]
        tasks_parsed = [{**t, "due_date": str(t["due_date"])} for t in raw]
        get_summary = generate_weekly_summary(tasks_parsed, user_name)
        summary = Summary(content=get_summary, user_id = user_id)
        session.add(summary)
        session.commit()
        session.refresh(summary)
        

@router.post("/generate", status_code=202)
def trigger_summary(
    background_tasks: BackgroundTasks,  # ← FastAPI injects this automatically
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    POST /summaries/generate
    Returns immediately. Summary is generated in the background.
    
    TODO:
    - Use background_tasks.add_task() to schedule _run_summary_generation
    - Pass: user_id=current_user.id, user_name=current_user.name
    - Return {"message": "Summary generation started"}
    
    Why 202 status code? Look it up — what does HTTP 202 mean semantically?
    """
    background_tasks.add_task(_run_summary_generation, 
                              user_id=current_user.id, 
                              user_name=current_user.name
    )
    return {"message": "Summary generation started"}
    

@router.get("/latest")
def get_latest_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    GET /summaries/latest
    Returns the most recently generated summary for the current user.
    
    TODO:
    - Query Summary where Summary.user_id == current_user.id
    - Order by created_at descending — get the newest one
      Hint: .order_by(Summary.created_at.desc()).first()
      OR: exec().all() then take [-1] ... which is safer?
    - If no summary found, raise 404
    - Return the summary
    """
    statement = select(Summary)\
      .where(Summary.user_id == current_user.id)\
      .order_by(Summary.created_at.desc())
    summary = db.exec(statement).first()
    if not summary:
        raise HTTPException(status_code=404, detail='No Summary Found')
    return summary