from pydantic import BaseModel 
from typing   import Optional , List
from pydantic import BaseModel 
from datetime import datetime

class User(BaseModel):
    user_name     : str
    display_name  : str


class UserDescribeResponse(BaseModel):
    name: str
    description: str
    creation_time: str


class UserTeamListResponse(BaseModel):
    teams: List[UserDescribeResponse]



#  Team 

class TeamCreateResponse(BaseModel):
    name: str
    description: Optional[str]
    admin: str

class TeamListResponse(BaseModel):
    name: str
    description: Optional[str]
    creation_time: datetime
    admin: str


class TeamUserListResponse(BaseModel):
    id: str
    name: str
    display_name: Optional[str]