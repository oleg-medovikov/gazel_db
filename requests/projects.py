
from .app import app

from models import User, Project, Project_access, Token, New_project 


@app.post("/allow_projects", tags=["projects"])
async def allow_projects(json : Token):
    "Получение списка доступных пользователю проектов"
    U_ID =  await User.token(json.token)
    try:
        res = await Project_access.list_projects(U_ID)
    except Exception:
        return {"error" : str(Exception)}
    else:
        if not res is None:
            projects = []
            for P_ID in res:
                projects.append(await Project.name(P_ID))
            return projects
        else:
            return []

@app.post("/create_project", tags=["projects"])
async def create_project (json : New_project ):
    "Создание нового проекта"
    res = await User.cheak_admin(json.token)
    if not res == True:
        return res
    else:
        U_ID = User.user_id(json.token)
        try:
            res = await Project.create(U_ID, json)
        except Exception:
            return {"error" : str(Exception)}
        else:
            json = {"token" : json.token, 
                    "p_id" : res['P_ID'],
                    "u_id" : U_ID,
                    "access_level" : 0 }
            try:
                res2 = await Project_access.add_access(json)
            except Exception:
                return {"error" : str(Exception)}
            else:
                return {"message" : "Проект успешно создан"}


