from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlmodel import Session

from models import Task, TaskCreate, TaskUpdate
from database import get_session
from services.tasks_services import (
    create_task,
    get_tasks,
    get_task_by_id,
    update_task,
    delete_task
)

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=Task, status_code=201)  # ya que tiene prefijo "/tasks", la ruta completa será "/tasks/"
def create_task_endpoint(
    task: TaskCreate,
    session: Session = Depends(get_session)
):
    return create_task(session, task)

@router.get("/", response_model=List[Task])
def get_tasks_endpoint(session: Session = Depends(get_session)):
    return get_tasks(session)


@router.get("/{task_id}", response_model=Task)
def get_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    task = get_task_by_id(session, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@router.put("/{task_id}", response_model=Task)
def update_task_endpoint(
    task_id: int,
    task: TaskUpdate,
    session: Session = Depends(get_session)
):
    updated_task = update_task(session, task_id, task)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task

@router.delete("/{task_id}", status_code=204)
def delete_task_endpoint(task_id: int, session: Session = Depends(get_session)):
    success = delete_task(session, task_id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")