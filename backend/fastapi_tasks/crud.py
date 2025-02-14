from sqlalchemy.orm import Session
from .models import Task

def get_tasks(db: Session):
    return db.query(Task).all()

def create_task(db: Session, title: str, description: str):
    new_task = Task(title=title, description=description)
    db.add(new_task)
    db.commit()
    return new_task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
