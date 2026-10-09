from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models import Base
from .routers import assessment
from .routers import assessment, quiz, dashboard, auth, teacher
from .routers import learning_dna
from .routers import revision
from .routers import doubt_solver

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Adaptive STEM Tutor API",
    description="AI-powered personalized STEM learning platform",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    assessment.router
)
app.include_router(
    quiz.router
)
app.include_router(dashboard.router)
app.include_router(auth.router)
app.include_router(teacher.router)
app.include_router(learning_dna.router)
app.include_router(revision.router)
app.include_router(doubt_solver.router)


@app.get("/")
def root():
    return {
        "message": "Adaptive STEM Tutor API is running",
        "status": "success"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }
