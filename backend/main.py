from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_project, delete_project, get_from_analyst

app = FastAPI()

#Allow requests from svelte 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/projects/create")
def createProject(name: str, owner: str):
    project = create_project(name, owner)
    if project:
        return {"message": "Project created", "project": project}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects/delete")
def deleteProject(name: str):
    project = delete_project(name)
    if project:
        return {"message": "Project marked as deleted", "project": project}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects/getFromAnalyst")
def getAnalystProjects(initials: str):
    projects = get_from_analyst(initials)
    return {"projects": projects}

@app.get("/api/projects/lock")
def lockProject():
    return {"Message": "Project locked"}

@app.get("/api/projects/unlock")
def unlockProject():
    return {"Message": "Project unlocked"}

@app.post("/api/projects/banish")
def banishProject():
    return {"Message": "Project banish"}

@app.post("/api/projects/restore")
def restoreProject():
    return {"Message": "Project restored"}

@app.post("/api/projects/join")
def joinProject():
    return {"message": "Joined project"}

@app.get("/api/projects/getFolders")
def getFolders():
    return {"message": "project folders"}

@app.post("/api/projects/deleteFolder")
def deleteFolder():
    return {"message": "deleted folder"}

@app.post("/api/projects/renameFolder")
def renameFolder():
    return {"message": "renamed folder"}