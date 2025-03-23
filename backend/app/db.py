# backend/app/db.py
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables from .env
load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def close_driver():
    driver.close()

def create_project(name: str, owner: str):
    query = """
        CREATE (p: Project {name: $name, owner: $owner})
        RETURN p
    """
    with driver.session() as session:
        result = session.run(query, name=name, owner=owner)
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
        WHERE p.deleted IS NOT NULL
        RETURN p.name AS name, p.owner AS owner
    """
    with driver.session() as session:
        result = session.run(query, initials=initials)
        return [record.data() for record in result]

