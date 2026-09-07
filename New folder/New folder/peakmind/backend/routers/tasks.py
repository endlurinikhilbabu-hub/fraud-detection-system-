from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
import sys
import os

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.ai_coach import suggest_task_priority

from database import get_session
from dependencies import get_current_user_id
from models import Task, EnergyLog

router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"]
)


@router.get("/suggest-priority")
def get_task_priority_suggestion(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
):
    # 1. Get all pending tasks
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id, Task.is_completed == False)
    ).all()
    if not tasks:
        return {"suggested_order": []}

    # 2. Get latest energy log
    latest_energy = session.exec(
        select(EnergyLog)
        .where(EnergyLog.user_id == user_id)
        .order_by(EnergyLog.logged_at.desc())
    ).first()
    energy_score = latest_energy.score if latest_energy else 50

    # 3. Call AI Coach
    task_dicts = [{"id": t.id, "title": t.title, "priority": t.priority} for t in tasks]
    suggested_order = suggest_task_priority(task_dicts, energy_score)

    return {"suggested_order": suggested_order}


@router.get("/", response_model=List[Task])
def read_tasks(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
):
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks


@router.post("/", response_model=Task)
def create_task(
    task: Task,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
):
    task.user_id = user_id  # Enforce from token, never trust client
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: Task,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    task_data_dict = task_data.dict(exclude_unset=True)
    task_data_dict.pop("user_id", None)  # Prevent user_id tampering
    for key, value in task_data_dict.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id),
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    session.delete(task)
    session.commit()
    return {"ok": True}
