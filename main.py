from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.tasks import router as tasks_router
from sqlmodel import SQLModel
from database import engine
from models import Task

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicio de la aplicación
    SQLModel.metadata.create_all(engine)
    print("Base de datos creada")
    yield
    # Fin de la aplicación
    print("Aplicación finalizada")

app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)