from fastapi import HTTPException  
from ..models import models
from datetime import datetime
import json
import os 

def create_board(request, db):
    board = db.query(models.ProjectModel).filter_by(name=request.name).first()
    if board:
        raise HTTPException(status_code=400, detail='A board with this name already exists for the team')
    
    if len(request.name) > 64:
        raise HTTPException(status_code=400, detail='Maximum 64 characters allowed for board name')
    
    if len(request.description) > 128:
        raise HTTPException(status_code=400, detail='Maximum 128 characters allowed for board description')
    
    team = db.query(models.TeamModel).filter_by(id=request.team_id).first()
    if not team:
        raise HTTPException(status_code=400, detail='Invalid team ID')
    
    record = models.ProjectModel(
        name=request.name,
        description=request.description,
        team_id=request.team_id,
        creation_time=datetime.now(),
        status = 'OPEN',
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {'id': str(record.id)}


def list_boards(db):
    all_boards = db.query(models.ProjectModel).all()
    return all_boards


def add_task(request, db):
    user = db.query(models.UserModel).filter_by(id=request.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail='Invalid user ID')

    teams = user.teams
    if not teams:
        raise HTTPException(status_code=400, detail='User is not a member of any team')

    project = None
    for team in teams:
        for proj in team.projects:
            if proj.status == 'OPEN' and user in team.members:
                project = proj
                break
        if project:
            break

    if not project:
        raise HTTPException(status_code=400, detail='User is not a member of any open board')

    task = db.query(models.TaskModel).filter_by(name=request.title, project_id=project.id).first()
    if task:
        raise HTTPException(status_code=400, detail='A task with this name already exists for the board')

    if len(request.title) > 64:
        raise HTTPException(status_code=400, detail='Maximum 64 characters allowed for task name')

    if len(request.description) > 128:
        raise HTTPException(status_code=400, detail='Maximum 128 characters allowed for task description')

    record = models.TaskModel(
        name=request.title,
        description=request.description,
        user_id=request.user_id,
        project_id=project.id,
        creation_time=datetime.now(),
        status='OPEN'
    )

    # Add the record to the database and commit the transaction
    db.add(record)
    db.commit()
    db.refresh(record)

    # Return the ID of the newly created task
    return {'id': str(record.id)}



def update_task_status(request,db):
    task_id = request.task_id
    new_status = request.status

    if not task_id or not new_status:
        raise HTTPException(status_code=400, detail='Invalid request')

    task = db.query(models.TaskModel).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail='Task not found')

    if new_status not in ['OPEN', 'IN_PROGRESS', 'COMPLETE']:
        raise HTTPException(status_code=400, detail='Invalid status')

    task.status = new_status
    db.commit()

    return {'message': 'Task status updated successfully'}


def list_tasks(project_id, db):
    """
    List all tasks for a specific project.
    """
    project = db.query(models.ProjectModel).filter_by(id=project_id).first()
    if not project:
        raise HTTPException(status_code=400, detail='Invalid project ID')

    tasks = project.tasks

    if not tasks:
        raise HTTPException(status_code=400, detail='No tasks found for the project')

    task_list = []
    for task in tasks:
        task_dict = {
            'id': str(task.id),
            'name': task.name,
            'description': task.description,
            'user_id': str(task.user_id),
            'status': task.status,
            'creation_time': task.creation_time,
        }
        task_list.append(task_dict)

    return task_list


def close_board(id, db):
    board = db.query(models.ProjectModel).filter_by(id=id).first()
    if not board:
        raise HTTPException(status_code=404, detail='Board not found')

    open_tasks = db.query(models.TaskModel).filter_by(project_id=id, status='OPEN').all()
    if open_tasks:
        raise HTTPException(status_code=400, detail='Cannot close board with open tasks')

    board.status = 'CLOSED'
    board.end_time = datetime.now()
    db.commit()

    return {'message':'Board closed successfully'} , 200


def export_board(board_id,db): 
    if not board_id:
        raise HTTPException(status_code=400, detail="Invalid request")

    board = db.query(models.ProjectModel).filter_by(id=board_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    tasks = db.query(models.TaskModel).filter_by(project_id=board_id).all()

    board_data = {
        "name": board.name,
        "description": board.description,
        "creation_time": str(board.creation_time),
        "status": board.status,
        "tasks": []
    }

    for task in tasks:
        task_data = {
            "name": task.name,
            "description": task.description,
            "user_id": task.user_id,
            "creation_time": str(task.creation_time),
            "status": task.status
        }
        board_data["tasks"].append(task_data)

    board_json = json.dumps(board_data)

    out_dir = "out"
    out_file = f"{board.name}_{board.id}.txt"
    out_path = os.path.join(out_dir, out_file)

    # Write the JSON string into the output file
    with open(out_path, "w") as f:
        f.write(board_json)

    # Return the name of the output file
    return {"out_file": out_file}