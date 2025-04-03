import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.time import DateTime as Neo4jDateTime
from datetime import datetime

# Load environment variables from .env
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def to_iso(dt):
    if isinstance(dt, datetime):
        return dt.isoformat()
    elif isinstance(dt, Neo4jDateTime):
        return dt.to_native().isoformat()
    elif isinstance(dt, str):
        return dt  # assume already ISO
    else:
        return None

def close_driver():
    driver.close()

def create_project(name: str, owner_initials: str, date: str, time: str, description: str):
    query = """
        MATCH (a:Analyst {initials: $owner_initials})
        CREATE (p:Project {
            name: $name,
            startDate: $date,
            startTime: $time,
            description: $description,
            deleted: false,
            owner: $owner_initials,
            lastEdit: datetime(), 
            locked: false
        })
        CREATE (a)-[:LEADS]->(p)
        RETURN p, a.initials AS owner
    """
    with driver.session() as session:
        result = session.run(query, {
            "name": name,
            "owner_initials": owner_initials,
            "date": date,
            "time": time,
            "description": description
        })
        record = result.single()
        return dict(record["p"]) if record else None

def update_project(name: str, owner_initials: str, date: str, time: str, description: str, id: int):
    query = """
        MATCH (p:Project)
        WHERE ID(p) = $id
        OPTIONAL MATCH (oldOwner:Analyst)-[r:LEADS]->(p)
        DELETE r
        WITH p
        MATCH (newOwner:Analyst {initials: $owner_initials})
        SET p.name = $name,
            p.startDate = $date,
            p.startTime = $time,
            p.description = $description,
            p.owner = $owner_initials,
            p.lastEdit = datetime()
        CREATE (newOwner)-[:LEADS]->(p)
        RETURN p, newOwner.initials AS owner
    """

    with driver.session() as session:
        result = session.run(query, {
            "id": id,
            "name": name,
            "owner_initials": owner_initials,
            "date": date,
            "time": time,
            "description": description
        })
        record = result.single()
        return dict(record["p"]) if record else None


def delete_project(name: str):
    query = """
        MATCH (p:Project {name: $name})
        SET p.deleted = true
        RETURN p
    """
    with driver.session() as session:
        result = session.run(query, name=name)
        record = result.single()
        return dict(record["p"]) if record else None
    
def get_from_analyst(initials: str):
    query = """
        MATCH (a:Analyst {initials: $initials})-[:ANALYST_ON|LEADS]->(p:Project)
        WHERE p.deleted = false
        RETURN p.description as description, ID(p) AS id, p.name AS name, p.owner AS owner, p.lastEdit AS lastEdit, p.locked AS locked
    """
    with driver.session() as session:
        result = session.run(query, initials=initials)
        return [{
            "name": record["name"],
            "owner": record["owner"],
            "editTime": to_iso(record["lastEdit"]),
            "locked": record["locked"],
            "id": record["id"],
            "description": record["description"],
        } for record in result]

def get_from_analyst_deleted(initials: str):
    query = """
        MATCH (a:Analyst {initials: $initials})-[:ANALYST_ON|LEADS]->(p:Project)
        WHERE p.deleted = true
        RETURN ID(p) AS id, p.name AS name, p.owner AS owner, p.lastEdit AS lastEdit
    """
    with driver.session() as session:
        result = session.run(query, initials=initials)
        return [{
            "name": record["name"],
            "owner": record["owner"],
            "editTime": to_iso(record["lastEdit"]),
            "id": record["id"],
        } for record in result]

def lock_project(name: str):
    query = """
        MATCH(p:Project {name: $name})
        SET p.locked = true
        RETURN p
    """
    with driver.session() as session:
        result = session.run(query, name=name)
        record = result.single()
        return dict(record["p"]) if record else None
    
def unlock_project(name: str):
    query = """
        MATCH(p:Project {name: $name})
        SET p.locked = false
        RETURN p
    """
    with driver.session() as session:
        result = session.run(query, name=name)
        record = result.single()
        return dict(record["p"]) if record else None
    
def banish_project(name: str):
    query = """
        MATCH (p:Project {name: $name})
        DETACH DELETE p
    """
    with driver.session() as session:
        session.run(query, name=name)
    return 1

def restore_project(name: str):
    query = """
        MATCH (p:Project {name: $name})
        SET p.deleted = false
        RETURN p
    """
    with driver.session() as session:
        result = session.run(query, name=name)
        record = result.single()
        return dict(record["p"]) if record else None
    
def join_project_by_id(initials: str, project_id: str) -> bool:
    query = """
        MATCH (a:Analyst {initials: $initials}), (p:Project {projectId: $project_id})
        MERGE (a)-[:JOINS]->(p)
        RETURN a.initials AS analyst, p.projectId AS project
    """
    with driver.session() as session:
        result = session.run(query, initials=initials, project_id=project_id)
        return result.single() is not None

def get_folders_by_project_id(project_id: str):
    query = """
        MATCH (:Project {projectId: $project_id})-[:HAS_FOLDER]->(f:ProjectFolder)
        RETURN f.name AS name
    """
    with driver.session() as session:
        result = session.run(query, project_id=project_id)
        return [record["name"] for record in result]

def delete_folder_by_name(folder_name: str) -> bool:
    query = """
        MATCH (f:ProjectFolder {name: $folder_name})
        DETACH DELETE f
        RETURN COUNT(f) > 0 AS deleted
    """
    with driver.session() as session:
        result = session.run(query, folder_name=folder_name)
        record = result.single()
        return record["deleted"] if record else False

def rename_folder_by_name(old_name: str, new_name: str) -> bool:
    query = """
        MATCH (f:ProjectFolder {name: $old_name})
        SET f.name = $new_name
        RETURN f.name AS updated_name
    """
    with driver.session() as session:
        result = session.run(query, old_name=old_name, new_name=new_name)
        record = result.single()
        return record is not None

# ---------------------------
# Analyst-related functions
# ---------------------------

def create_or_update_analyst(initials: str, is_lead: bool):
    """
    Creates a new analyst or updates an existing one.
    Sets the role to "Lead" if is_lead is True; otherwise "Regular".
    """
    role = "Lead" if is_lead else "Regular"
    query = """
    MERGE (a:Analyst {initials: $initials})
    SET a.role = $role
    RETURN a.initials AS initials, a.role AS role
    """
    with driver.session() as session:
        result = session.run(query, initials=initials, role=role)
        record = result.single()
        return {"initials": record["initials"], "role": record["role"]} if record else None

def is_lead_analyst(project_name: str, initials: str) -> bool:
    """
    Checks if the analyst with given initials is the lead for the project.
    """
    query = """
    MATCH (p:Project {name: $project_name})<-[:LEADS]-(a:Analyst {initials: $initials})
    RETURN COUNT(p) > 0 AS is_lead
    """
    with driver.session() as session:
        result = session.run(query, project_name=project_name, initials=initials)
        record = result.single()
        return record["is_lead"] if record else False

def leave_project(initials: str, project_name: str) -> bool:
    """
    Removes the relationship between the analyst and the project.
    Only non-leads should be allowed to leave.
    """
    query = """
    MATCH (p:Project {name: $project_name})<-[r:JOINS]-(a:Analyst {initials: $initials})
    DELETE r
    RETURN COUNT(r) AS deleted
    """
    with driver.session() as session:
        result = session.run(query, project_name=project_name, initials=initials)
        record = result.single()
        return record["deleted"] > 0 if record else False

def get_projects_with_analysts():
    """
    Retrieves all projects along with their lead analyst and any regular analysts who have joined.
    """
    query = """
    MATCH (p:Project)<-[:LEADS]-(l:Analyst)
    OPTIONAL MATCH (p)<-[r:JOINS]-(a:Analyst)
    RETURN p.name AS project_name, l.initials AS lead_analyst, p.locked AS locked, COLLECT(a.initials) AS regular_analysts
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]
