from fastapi import HTTPException  
from ..models import models
from datetime import datetime

def create_team(request,db):
    teamname = db.query(models.TeamModel).filter_by(name=request.name).first()

    if teamname:
        raise HTTPException(status_code=400, detail='there is already a team present with this name ')
    
    if len(request.name) > 64:
        raise HTTPException(status_code=400, detail='max character allowed is 64 chars')
    
    team_name = request.name
    team_desc  = request.description
    create_date  = datetime.now()
    admin_id     = request.admin

    db_user  = db.query(models.UserModel).filter_by(id=admin_id).first()

    if not db_user: 
        raise HTTPException(status_code=400, detail='please enter valid admin id ')

    record = models.TeamModel(
        name =  team_name,
        description = team_desc,
        creation_time = create_date,
        admin_id = admin_id,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {'id': str(record.id)}, 200


def get_all_teams(db):
    all_teams = db.query(models.TeamModel).all()
    return all_teams

def desc_team(id, db):
    get_team = db.query(models.TeamModel).filter_by(id= id).first()

    if not get_team:
        raise HTTPException(status_code=400, detail=f'there is no team present with this {id} ')

    return get_team


def update_team(id,request,db):
    get_team= db.query(models.TeamModel).filter_by(id= id).first()

    if not get_team:
        raise HTTPException(status_code=404, detail=f'there is no team present with this {id} ') 
    
    if request.name != get_team.name:
        raise HTTPException(status_code=404, detail=f'team name cant be changed ')
     
    get_team.admin_id = request.admin
    get_team.description = request.description

    db.commit()

    return {'message': f'Team {get_team.name} been successfully updated'} , 200


def add_users_to_team(request, db):
    team = db.query(models.TeamModel).filter(models.TeamModel.id == request.team_id).first()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    users = db.query(models.UserModel).filter(models.UserModel.id.in_(request.users)).all()

    if not users:
        raise HTTPException(status_code=404, detail = ' there are no users present with these ids')
    
    team.members.extend(users)
    db.commit()
    return {"message": "Users added to team successfully"}


def remove_users_from_team(request, db):
    team = db.query(models.TeamModel).filter(models.TeamModel.id == request.team_id).first()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    users = db.query(models.UserModel).filter(models.UserModel.id.in_(request.users)).all()

    # Remove the users from the team
    user_ids_to_remove = set(user.id for user in users)
    team.members = [member for member in team.members if member.id not in user_ids_to_remove]

    db.commit()
    return {"message": "Users removed from team successfully"}


def list_team_users(team_id, db):
    # Check if the team exists in the database
    team = db.query(models.TeamModel).filter(models.TeamModel.id == team_id).first()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Get the user objects that belong to the team
    team_users = [user for user in team.members]
    
    return team_users