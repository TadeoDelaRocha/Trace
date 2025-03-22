import neo4j from 'neo4j-driver';

const URI = process.env.NEO4J_URI || 'bolt://localhost:7687';
const USER = process.env.NEO4J_USER || 'neo4j';
const PASSWORD = process.env.NEO4J_PASSWORD || 'dj897wryfsac!#';

const driver = neo4j.driver(URI, neo4j.auth.basic(USER, PASSWORD));

export default driver;
