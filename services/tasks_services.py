from sqlmodel import Session, select
from models import Task, TaskCreate, TaskUpdate

def create_task(session: Session, task: TaskCreate) -> Task:
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def get_tasks(session: Session) -> list[Task]:
    statement = select(Task)
    return session.exec(statement).all()


def get_task_by_id(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)


def update_task(session: Session, task_id: int, task: TaskUpdate) -> Task | None:
    db_task = session.get(Task, task_id)

    if not db_task:
        return None

    task_data = task.model_dump(exclude_unset=True)

    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(Task, task_id)

    if not task:
        return False

    session.delete(task)
    session.commit()

    return True