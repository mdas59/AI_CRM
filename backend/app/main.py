from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.database import engine, Base
from app import models

from app.routes import interactions
from app.routes import ai


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-First CRM HCP Module",
    description="Backend API for logging HCP interactions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React/Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interactions.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "AI CRM HCP backend is running"}