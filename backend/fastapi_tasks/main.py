from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
from .database import SessionLocal, engine
from .models import Base
from .crud import get_tasks, create_task, delete_task

Base.metadata.create_all(bind=engine)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    tasks = get_tasks(db)
    return templates.TemplateResponse("index.html", {"request": request, "tasks": tasks})

@app.post("/add-task/")
async def add_task(title: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    create_task(db, title, description)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)

@app.get("/delete-task/{task_id}")
async def remove_task(task_id: int, db: Session = Depends(get_db)):
    delete_task(db, task_id)
    return RedirectResponse("/", status_code=HTTP_303_SEE_OTHER)
