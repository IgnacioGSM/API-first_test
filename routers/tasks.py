from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate
from database import engine, get_session

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=Task, status_code=201)  # ya que tiene prefijo "/tasks", la ruta completa será "/tasks/"
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[Task])
def get_tasks(session: Session = Depends(get_session)):
    statement = select(Task)
    tasks = session.exec(statement).all()
    return tasks


@router.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)

    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()

    return Response(status_code=204)