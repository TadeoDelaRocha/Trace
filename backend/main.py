from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_project, delete_project, get_from_analyst, lock_project, unlock_project, banish_project, restore_project, get_from_analyst_deleted, join_project_by_id, get_folders_by_project_id, delete_folder_by_name, rename_folder_by_name

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
        raise HTTPException(status_code=404, detail="Project not created")

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

@app.post("/api/projects/getFromAnalystDeleted")
def getAnalystProjects(initials: str):
    projects = get_from_analyst_deleted(initials)
    return {"projects": projects}

@app.get("/api/projects/lock")
def lockProject(name: str):
    project = lock_project(name)
    if project:
        return {"message": "Project locked", "project": project}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.get("/api/projects/unlock")
def unlockProject(name: str):
    project = unlock_project(name)
    if project:
        return {"message": "Project unlocked", "project": project}
    else:
        raise HTTPException(status_code=404, detail="Project not found")

@app.post("/api/projects/banish")
def banishProject(name: str):
    banish_project(name)
    return {"message": "Project banished"}

@app.post("/api/projects/restore")
def restoreProject(name: str):
    project = restore_project(name)
    if project:
        return {"message": "Project restored", "project": project}
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
