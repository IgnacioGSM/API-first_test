from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")