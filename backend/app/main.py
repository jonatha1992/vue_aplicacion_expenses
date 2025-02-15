from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import expenses, categories
from .database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vue dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers without prefix (prefix is in routes)
app.include_router(expenses.router)
app.include_router(categories.router)

# Root endpoint for API health check
@app.get("/")
async def root():
    return {"status": "active", "message": "Welcome to the Expenses API"}