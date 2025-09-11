import uuid 
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status,Cookie,Response,BackgroundTasks
from datetime import datetime
from sqlalchemy.orm import Session

from db.database import get_db, sessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import(
    CompleteStoryResponse,CompleteStoryNodeResponse,CreateStoryRequest
)
from schemas.job import StoryJobCreate,StoryJobResponse
from core.story_generator import StoryGenerator

router = APIRouter(
    prefix ="/stories",
    tags = ["stories"]
)

def get_session_id(session_id:Optional[str]=Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request:CreateStoryRequest,
    response:Response,
    background_tasks:BackgroundTasks,
    session_id:str = Depends(get_session_id),
    db :Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    #Creat  a new story job
    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status="pending"
    )
    db.add(job)
    db.commit()

    #TODO: Add background task to process the story generation
    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )
    return job

def generate_story_task(job_id:str,theme:str,session_id:str):
    db = sessionLocal()

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id==job_id).first()

        if not job:
            return
        try:
            job.status = "processing"
            db.commit()

            story= StoryGenerator.generate_story(db,session_id,theme)
            job.story_id = story.id 

            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()

@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id:int,db:Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id==story_id).first()
    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    
    #Todo: parse story to complete format
    complete_story = build_complete_story_tree(db, story)
    return complete_story

def build_complete_story_tree(db:Session, story:Story)->CompleteStoryResponse:
    #Retrieve all nodes from the story
    nodes = db.query(StoryNode).filter(StoryNode.story_id==story.id).all()

    node_dict = {}
    for node in nodes:
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_good_ending=node.is_good_ending,
            options=node.options
        )
        node_dict[node.id] = node_response
    #Find the root node
    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        raise HTTPException(status_code=500, detail="Story root node not found")
    
    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict

    )
