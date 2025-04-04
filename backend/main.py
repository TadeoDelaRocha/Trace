from fastapi import HTTPException, FastAPI
from pydantic import BaseModel

from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

from app.db import (
    create_project, delete_project, get_from_analyst, lock_project, unlock_project,
    banish_project, restore_project, get_from_analyst_deleted, join_project_by_id,
    get_folders_by_project_id, delete_folder_by_name, rename_folder_by_name,
    create_or_update_analyst, is_lead_analyst, leave_project, get_projects_with_analysts
)

from app.db import create_project, update_project, delete_project, get_from_analyst, lock_project, unlock_project, banish_project, restore_project, get_from_analyst_deleted, join_project_by_id, get_folders_by_project_id, delete_folder_by_name, rename_folder_by_name


import json
import httpx

app = FastAPI()

class ProjectNamePayload(BaseModel):
    toEdit: str

class ProjectPayload(BaseModel):
    name: str
    date: str
    time: str
    owner: str
    description: str


class ProjectUpdatePayload(BaseModel):
    name: str
    date: str
    time: str
    owner: str
    description: str
    id: int


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #TODO(Team 12 - Jorge): Changed as ports can be different
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/projects/create")
def createProject(project: ProjectPayload):
    result = create_project(
        name=project.name,
        owner_initials=project.owner,
        date=project.date,
        time=project.time,
        description=project.description
    )

    if result:
        return {"message": "Project created successfully", "project": result}
    else:
        raise HTTPException(status_code=500, detail="Failed to create project")

@app.post("/api/projects/update")
def updateProject(project: ProjectUpdatePayload):
    print("UPDATE REQUEST:", project)
    result = update_project(
        name=project.name,
        owner_initials=project.owner,
        date=project.date,
        time=project.time,
        description=project.description,
        id=project.id
    )
    print("UPDATED:", result)

    if result:
        return {"message": "Project updated successfully", "project": result}
    else:
        raise HTTPException(status_code=500, detail="Failed to update project")

@app.post("/api/projects/delete")
def deleteProject(payload: ProjectNamePayload):
    name = payload.toEdit
    project = delete_project(name)
    if project:
        return {"message": "Project marked as deleted", "project": project}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects/getFromAnalyst")
def getAnalystProjects(initials: str):
    projects = get_from_analyst(initials)
    return {"projects": projects}

@app.post("/api/projects/getFromAnalystDeleted")
def getAnalystProjects(initials: str):
    projects = get_from_analyst_deleted(initials)
    return {"projects": projects}

@app.post("/api/projects/lock")
def lockProject(payload: ProjectNamePayload):
    name = payload.toEdit
    project = lock_project(name)
    if project:
        return {"message": "Project locked", "project": project}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects/unlock")
def unlockProject(payload: ProjectNamePayload):
    name = payload.toEdit
    project = unlock_project(name)
    if project:
        return {"message": "Project unlocked", "project": project}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects/banish")
def banishProject(payload: ProjectNamePayload):
    name = payload.toEdit
    result = banish_project(name)
    if result == 1:
        return {"message": "Project banished forever"}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects/restore")
def restoreProject(payload: ProjectNamePayload):
    name = payload.toEdit
    project = restore_project(name)
    if project:
        return {"message": "Project marked as deleted", "project": project}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects/join")
def join_project(project_id: str, analyst_initials: str):
    joined = join_project_by_id(analyst_initials, project_id)
    if joined:
        return {"message": f"Analyst {analyst_initials} joined project {project_id}"}
    else:
        raise HTTPException(status_code=404, detail="Analyst or Project not found")

@app.get("/api/projects/getFolders")
def get_folders(project_id: str):
    folders = get_folders_by_project_id(project_id)
    return {"folders": folders}

@app.post("/api/projects/deleteFolder")
def delete_folder(folder_name: str):
    deleted = delete_folder_by_name(folder_name)
    if deleted:
        return {"message": f"Folder '{folder_name}' deleted"}
    else:
        raise HTTPException(status_code=404, detail="Folder not found")

@app.post("/api/projects/renameFolder")
def rename_folder(old_name: str, new_name: str):
    renamed = rename_folder_by_name(old_name, new_name)
    if renamed:
        return {"message": f"Folder renamed from '{old_name}' to '{new_name}'"}
    else:
        raise HTTPException(status_code=400, detail="Rename failed or folder not found")


# ---------------------------
# Analyst-related Endpoints
# ---------------------------

class AnalystLoginPayload(BaseModel):
    initials: str
    is_lead: bool

@app.post("/api/analyst/login")
def analyst_login(payload: AnalystLoginPayload):
    result = create_or_update_analyst(payload.initials, payload.is_lead)
    if result:
        return {"message": "Login successful", "analyst": result}
    else:
        raise HTTPException(status_code=500, detail="Login failed")

class LeaveProjectPayload(BaseModel):
    project_name: str
    initials: str

@app.post("/api/analyst/leave")
def analyst_leave(payload: LeaveProjectPayload):
    # Prevent lead analysts from leaving their own projects.
    if is_lead_analyst(payload.project_name, payload.initials):
        raise HTTPException(status_code=403, detail="Lead cannot leave the project")
    success = leave_project(payload.initials, payload.project_name)
    if success:
        return {"message": f"Analyst {payload.initials} left project {payload.project_name}"}
    else:
        raise HTTPException(status_code=404, detail="Analyst or project not found")

@app.get("/api/analyst/list_projects")
def list_projects_analysts():
    projects = get_projects_with_analysts()
    return {"projects": projects}

@app.post("/proxy")
async def proxy_handler(request: Request):
    try:
        #Gets info that will be sent to proxy
        payload = await request.json()
        url = payload.get("url")
        method = payload.get("method", "GET").upper()
        headers = payload.get("headers", {})
        body = payload.get("body", None)
        cookies = payload.get("cookies", None)
        params = payload.get("params", None)

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                content=body,
                cookies=cookies,
                params=httpx.QueryParams(params) if params else None
            )

        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text
        }

    except Exception as e:
        import traceback
        print("Proxy error:\n", traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "Failed to process proxy request"
            }
        )

