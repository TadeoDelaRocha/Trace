# backend/app/db.py
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.time import DateTime as Neo4jDateTime
from datetime import datetime


# Load environment variables from .env
load_dotenv()

NEO4J_URI = "neo4j+ssc://cc549e3f.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "qqBUQoAIi6DwzKIU22y4mYP9ZKo6PrbkA3q6yPJwfrg"

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
        RETURN p.name AS name, p.owner AS owner, p.lastEdit AS lastEdit, p.locked AS locked
    """
    with driver.session() as session:
        result = session.run(query, initials=initials)
        return [{
            "name": record["name"],
            "owner": record["owner"],
            "editTime": to_iso(record["lastEdit"]),
            "locked": record["locked"]
        } for record in result]

def get_from_analyst_deleted(initials: str):
    query = """
        MATCH (a:Analyst {initials: $initials})-[:ANALYST_ON|LEADS]->(p:Project)
        WHERE p.deleted = true
        RETURN p.name AS name, p.owner AS owner, p.lastEdit AS lastEdit
    """
    with driver.session() as session:
        result = session.run(query, initials=initials)
        return [{
            "name": record["name"],
            "owner": record["owner"],
            "editTime": to_iso(record["lastEdit"])
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
