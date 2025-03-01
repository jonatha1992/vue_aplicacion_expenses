from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth_routes, category_routes, expense_routes
from .database import Base, engine
import os
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

# Configuración CORS actualizada
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://expenses-traker-f3fcc.web.app", 
        "http://localhost:8000",  # Firebase hosting URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers without prefix (prefix is in routes)
app.include_router(expense_routes.router)
app.include_router(category_routes.router)
app.include_router(auth_routes.router)

# Root endpoint for API health check
@app.get("/")
async def root():
    return {"status": "active", "message": "Welcome to the Expenses API"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Cloud Run usa PORT=8080
    uvicorn.run(app, host="0.0.0.0", port=port)