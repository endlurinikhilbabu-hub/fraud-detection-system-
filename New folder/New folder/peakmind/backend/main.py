from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="PeakMind AI Backend",
    description="Backend API for PeakMind AI Performance Coach",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database import create_db_and_tables
from routers import tasks, energy

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(tasks.router)
app.include_router(energy.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "PeakMind AI backend is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
