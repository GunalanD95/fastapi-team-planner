import sys
sys.path.append("...") 

from db.db import Base
from sqlalchemy import Column, Integer, String, DateTime , Float , Sequence ,  ForeignKey , Table
from sqlalchemy.orm import relationship 


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