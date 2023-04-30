import sys
sys.path.append("...") 

from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime , Float , Sequence ,  ForeignKey , Table
from sqlalchemy.orm import relationship 
from enum import Enum


# Association table for user-team relationship
team_users = Table('team_users', Base.metadata,
                   Column('team_id', Integer, ForeignKey('teams.id')),
                   Column('user_id', Integer, ForeignKey('users.id'))
                   )


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True)
    display_name = Column(String(64))
    creation_time = Column(DateTime)
    teams = relationship("TeamModel", secondary=team_users, back_populates="members")


class TeamModel(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True)
    description = Column(String(128))
    creation_time = Column(DateTime)
    admin_id = Column(Integer, ForeignKey('users.id'))

    # Define one-to-many relationship between Team and User models
    members = relationship("UserModel", secondary=team_users, back_populates="teams")
    projects = relationship("ProjectModel", back_populates="team")




class ProjectModel(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, index=True)
    description = Column(String(128))
    creation_time = Column(DateTime)
    team_id = Column(Integer, ForeignKey('teams.id'))
    status    = Column(String,default='Open')
    tasks = relationship("TaskModel", back_populates="project")
    team = relationship("TeamModel", back_populates="projects")
    end_time = Column(DateTime)


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), index=True)
    description = Column(String(128))
    creation_time = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

    project = relationship("ProjectModel", back_populates="tasks")
    status    = Column(String,default='Open')