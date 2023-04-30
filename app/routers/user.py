import sys
sys.path.append("...") 

from fastapi import APIRouter ,  Depends  
# importing the db connection
from db.db import  get_db
from ..schemas.schemas import User , UserDescribeResponse , UserTeamListResponse , TeamListResponse
from sqlalchemy.orm import Session
from ..repos import user

user_router = APIRouter(
    tags=['user'],
)


@user_router.post('/user',status_code= 200)
async def create_user(request: User , db: Session = Depends(get_db)):
    return user.create_user(request,db)


@user_router.get('/users')
async def get_all_users(db: Session = Depends(get_db)):
    return user.get_all_users(db)


@user_router.get('/users/{id}')
async def desc_user(id: int , db: Session = Depends(get_db)):
    return user.desc_user(id,db)


@user_router.patch('/users/{id}')
async def update_user(id: int ,request: User , db: Session = Depends(get_db)):
    return user.update_user(id,request,db)

@user_router.get('/user/team/{id}')
async def get_user_teams(id: int , db: Session = Depends(get_db)):
    return user.get_user_teams(id,db,TeamListResponse)