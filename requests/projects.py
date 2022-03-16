
from .app import app
from fastapi import Header, Body
from typing import Optional

from models import User, Project, Project_access


@app.get("/allow_projects", tags=["projects"])
async def allow_projects(
        Authorization : Optional[str] = Header(None)):
    "Получение списка доступных пользователю проектов"
    if Authorization is None:
        return None
    U_ID =  await User.user_id(Authorization)
    try:
        res = await Project_access.list_projects(U_ID)
    except Exception as e:
        return {"error" : str(e)}
    else:
        if not res is None:
            projects = []
            for P_ID in res:
                projects.append(await Project.name(P_ID))
            return projects
        else:
            return []

@app.post("/create_project", tags=["projects"])
async def create_project (
        Authorization: Optional[str] = Header(None),
        p_name: Optional[str] = Body(None),
        p_description: Optional[str] = Body(None)
        ):
    "Создание нового проекта"
    if Authorization is None or p_name is None or p_description is None:
        return None

    res = await User.cheak_admin(Authorization)
    if not res == True:
        return res
    else:
        U_ID = await User.user_id(Authorization)
        try:
            res = await Project.create(U_ID, p_name, p_description)
        except Exception as e:
            return {"error" : str(e)}
        else:
            if  hasattr(res, "error"):
                return res
            else:

                try:
                    res2 = await Project_access.add_access(
                            res["p_id"],
                            U_ID,
                            0
                            )
                except Exception as e:
                    return {"error" : str(e)}
                else:
                    return res2

@app.get("/project_info", tags=["projects"])
async def get_project_info(
        Authorization: Optional[str] = Header(None),
        p_name: Optional[str] = Body(None)
        ):
    "Узнаем описание проекта"
    if Authorization is None or p_name is None:
        return None

    res = await User.cheak_token(Authorization)
    
    if not res == True:
        return res
    else:
        return await Project.get_project(p_name)

@app.get("/list_team_users", tags=["projects"])
async def list_team_users(
        Authorization: Optional[str] = Header(None),
        p_name: Optional[str] = Body(None)
        ):
    "Получаем список причастных к проекту пользователей"
    res = await User.cheak_token(Authorization)
    if not res == True:
        return res
    else:
        res  = await Project.get_project(p_name)
        users = await Project_access.list_users(res["p_id"])

        list_ = []

        for u in users:
            name = await User.name_user(u["u_id"])
            list_.append( name )

        return list_

@app.post("/add_user_to_team", tags=["projects"])
async def add_user_to_team(
        Authorization: Optional[str] = Header(None),
        author: Optional[str] = Body(None),
        p_name: Optional[str] = Body(None),
        username: Optional[str] = Body(None),
        access_level: Optional[int] = Body(None)
        ):
    "Добавляем пользователя в команду проекта"
    if Authorization is None \
            or author is None \
            or p_name is None \
            or username is None \
            or access_level is None:
        return None

    res = await User.cheak_token(Authorization)
    
    if not res == True:
        return res
 
    res = await Project.get_project(p_name)
    u_id = await User.user_id(author)

    if not res is None:
        if not res["u_id"] == u_id:
            return {"error" : "Вы не являетесь автором проекта"}
        else:
            USER_ID = await User.user_id(username)
            PROJECT_ID = await Project.id(p_name)
            res = await Project_access.add_access(PROJECT_ID,USER_ID,access_level)

            return res


@app.delete("/remove_user_from_team", tags=["projects"])
async def remove_user_from_team(
        Authorization: Optional[str] = Header(None),
        p_name: Optional[str] = Body(None),
        username: Optional[str] = Body(None)
        ):
    "удаляем пользователя из команды проекта"
    if Authorization is None \
            or p_name is None \
            or username is None :
        return None

    U_ID = await User.user_id(Authorization)
    res = await Project.get_project(p_name)
    removed_user = await User.user_id(username)

    if not res is None:
        if res['u_id'] == removed_user:
            return {"error" : "Нельзя удалить создателя проекта"}
        else:
            if await User.cheak_admin(Authorization) == True \
                    or res['u_id'] == U_ID:
                res2 = await Project_access.remove_access(
                                res['p_id'],
                                removed_user
                        )
                return res2
