from fastapi import FastAPI
from .database import engine
from .models import Base
from .routes import expenses

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(expenses.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Expenses API"}