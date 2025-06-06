import os
from pymongo import MongoClient
from neo4j import GraphDatabase

class Config:
    # Configuration MongoDB
    MONGO_URI = "mongodb://localhost:27017/"
    MONGO_DB_NAME = "cabinet_db"

    # Configuration Neo4j
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "cabinet123"  # Remplacez par votre mot de passe Neo4j

    # Configuration Flask
    SECRET_KEY = "votre_cle_secrete_ici"
    SESSION_PERMANENT = False

class DatabaseConnections:
    _mongo_client = None
    _neo4j_driver = None

    @classmethod
    def get_mongo_db(cls):
        """Connexion à MongoDB"""
        if cls._mongo_client is None:
            cls._mongo_client = MongoClient(Config.MONGO_URI)
        return cls._mongo_client[Config.MONGO_DB_NAME]

    @classmethod
    def get_neo4j_driver(cls):
        """Connexion à Neo4j"""
        if cls._neo4j_driver is None:
            cls._neo4j_driver = GraphDatabase.driver(
                Config.NEO4J_URI,
                auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD)
            )
        return cls._neo4j_driver

    @classmethod
    def close_connections(cls):
        """Fermer les connexions"""
        if cls._mongo_client:
            cls._mongo_client.close()
        if cls._neo4j_driver:
            cls._neo4j_driver.close()