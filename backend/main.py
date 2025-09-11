from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import story, job
from core.config import settings
from db.database import create_tables

create_tables() #create database tables if not exist
app = FastAPI(
    title ="StoryGenerator API",
    description="API for generating stories using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], #allow use any API method
    allow_headers=["*"],)

app.include_router(story.router,prefix=settings.API_PREFIX)
app.include_router(job.router,prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}