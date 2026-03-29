from sqlmodel import SQLModel, Field

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=255)
    completed: bool = False

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    model_config = {
        "from_attributes": True     # permite crear un objeto Task a partir de un objeto TaskCreate usando el método model_validate
    }

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None