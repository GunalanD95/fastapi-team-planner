import sys
sys.path.append("...") 

from fastapi import APIRouter ,  Depends  
# importing the db connection
from db.db import  get_db
from sqlalchemy.orm import Session
from ..schemas.schemas import TeamCreateResponse , AddUserTeam , RemoveUserTeam
from ..repos import team

team_router = APIRouter(
    tags=['team'],
)


@team_router.post('/team', status_code=200)
async def create_team(request: TeamCreateResponse, db: Session = Depends(get_db)):
    return team.create_team(request, db)


@team_router.get('/teams')
async def get_all_teams(db: Session = Depends(get_db)):
    return team.get_all_teams(db)


@team_router.get('/teams/{id}')
async def describe_team(id: int, db: Session = Depends(get_db)):
    return team.desc_team(id, db)


@team_router.patch('/teams/{id}')
async def update_team(id: int ,request: TeamCreateResponse , db: Session = Depends(get_db)):
    return team.update_team(id, request, db)


@team_router.post('/teams/{id}/users')
async def add_users_to_team(request: AddUserTeam, db: Session = Depends(get_db)):
    return team.add_users_to_team(request, db)


@team_router.delete('/teams/{id}/users')
async def remove_users_from_team(request : RemoveUserTeam, db: Session = Depends(get_db)):
    return team.remove_users_from_team(request, db)


@team_router.get('/teams/{id}/users')
async def list_team_users(id: int, db: Session = Depends(get_db)):
    return team.list_team_users(id, db)
