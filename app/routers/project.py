import sys
sys.path.append("...") 

from fastapi import APIRouter ,  Depends  
# importing the db connection
from db.db import  get_db
from sqlalchemy.orm import Session
from ..schemas.schemas import BoardCreateResponse , TaskCreateRequest , UpdateTask
from ..repos import project

project_router = APIRouter(
    tags=['project'],
)

@project_router.post('/board')
async def create_board(request: BoardCreateResponse, db: Session = Depends(get_db)):
    return project.create_board(request, db)

@project_router.patch('/board/close')
async def close_board(id: int, db: Session = Depends(get_db)):
    return project.close_board(id, db)

@project_router.post('/board/task')
async def add_task(request: TaskCreateRequest, db: Session = Depends(get_db)):
    return project.add_task(request, db)

@project_router.patch('/board/task')
async def update_task_status(request: UpdateTask, db: Session = Depends(get_db)):
    return project.update_task_status(request, db)

@project_router.get('/board/list', status_code=200)
async def list_boards(db: Session = Depends(get_db)):
    return project.list_boards(db)

@project_router.get('/board/{project_id}/tasks')
async def get_tasks_for_project(project_id: str, db: Session = Depends(get_db)):
    return project.list_tasks(project_id, db)

@project_router.get('/board/export', status_code=200)
async def export_board(id : int , db: Session = Depends(get_db)):
    return project.export_board(id, db)