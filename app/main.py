import sys
sys.path.append("..") 

from fastapi import FastAPI
from db import db
from .models import models
from .routers import user , team

app = FastAPI()



get_db = db.get_db()
models.Base.metadata.create_all(db.engine)


@app.get('/')
def home():
    return {'message': 'Check /docs Page'}


# register all routers
app.include_router(user.user_router)
app.include_router(team.team_router)