import sys
sys.path.append("...") 

from fastapi import APIRouter ,  Depends  
# importing the db connection
from db.db import  get_db
from ..schemas.schemas import User , UserDescribeResponse , UserTeamListResponse 
from sqlalchemy.orm import Session
from ..repos import user

user_router = APIRouter(
    tags=['user'],
)


@user_router.post('/user',status_code= 200)
async def CreateUser(request: User , db: Session = Depends(get_db)):
    return user.create_user(request,db)


@user_router.get('/users')
async def GetAllUsers(db: Session = Depends(get_db)):
    return user.get_all_users(db)


@user_router.get('/users/{id}')
async def GetUser(id: int , db: Session = Depends(get_db)):
    return user.desc_user(id,db)


@user_router.patch('/users/{id}')
async def UpdateUser(id: int ,request: User , db: Session = Depends(get_db)):
    return user.update_user(id,request,db)