from fastapi import HTTPException  
from ..models import models
from datetime import datetime
import json 


def create_user(request,db):
    username = db.query(models.UserModel).filter_by(name=request.user_name).first()

    if username:
        raise HTTPException(status_code=400, detail='there is already a user present with the username ')
    
    req_username = request.user_name
    req_display  = request.display_name
    create_date  = datetime.now()

    if len(req_username) > 64:
        return HTTPException(status_code=400, detail='Username Length should be lesser than 64 characters')
    
    record       = models.UserModel(
        name = req_username,
        display_name = req_display,
        creation_time = create_date,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {'id': str(record.id)}, 200


def get_all_users(db):
    all_users = db.query(models.UserModel).all()
    return all_users


def desc_user(id , db):
    get_user = db.query(models.UserModel).filter_by(id= id).first()

    if not get_user:
        raise HTTPException(status_code=400, detail=f'there is no user present with this {id} ')

    return get_user


def update_user(id,request,db):
    get_user = db.query(models.UserModel).filter_by(id= id).first()

    if not get_user:
        raise HTTPException(status_code=400, detail=f'there is no user present with this {id} ') 
    
    if request.user_name != get_user.name:
        raise HTTPException(status_code=400, detail=f'username cant be changed ')
     
    get_user.display_name = request.display_name
    db.commit()

    return {'message': f'User {get_user.name} been successfully updated'} , 200


def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"{type(obj)} not serializable")

def get_user_teams(user_id: int, db,TeamListResponse):
    user_teams = db.query(models.TeamModel).filter(models.TeamModel.members.any(id=user_id)).all()
    team_info  = [TeamListResponse(name=team.name, description=team.description, creation_time=team.creation_time,admin=team.admin_id) for team in user_teams]
    return team_info
      





