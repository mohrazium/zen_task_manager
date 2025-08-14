from typing import Optional

import yaml
from fastapi.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.config.database.base_table import BaseTable
from src.config.exceptions.failure_exception import FailureException


def _loadConfig()-> str:
        try:
            with open("src/config/database/db_config.yaml", "r") as file:
                config = yaml.safe_load(file)
                dbname = config.get("database", {}).get("name")
                user = config.get("database", {}).get("user")
                user_pass = config.get("database", {}).get("password")
                host = config.get("database", {}).get("host")
                port = config.get("database", {}).get("port")
                return f"postgresql+psycopg2://{user}:{user_pass}@{host}:{port}/{dbname}"
        except FileNotFoundError:
            raise FailureException(message="Database configuration file not found.")
        except Exception as e:
            raise FailureException(message="Error loading database configuration:", error=e)
    

def _configure():
    try:
        _databaseUrl = _loadConfig()
        engine = create_engine(_databaseUrl, echo=False)
        sessionFactory = sessionmaker(autoflush=False, autocommit=False, bind=engine)
        scopedSession = scoped_session(sessionFactory)
        logger.info("Database engine and session factory configured.")
        return engine, sessionFactory, scopedSession
    except Exception as e:
        logger.error("Error configuring database:", e)
        raise FailureException(message="Database configuration failed.", error=e)

class ZenTaskDatabase():
    def __init__(self):
        self._engine, self._sessionFactory, self._scopedSession = _configure()
    
    def initialize(self):
        if self._engine and self._sessionFactory and self._scopedSession:
            BaseTable.metadata.create_all(self._engine)
            logger.info("Database initialized successfully.")
        else:
            raise FailureException(message="Database initialization failed. Please check the configuration.")
        
    def getSession(self):
        if self._scopedSession:
            return self._scopedSession()
        else:
            raise FailureException(message="Session factory is not configured. Please initialize the database first.")
        
    def closeSession(self, session):
        if session:
            session.close()
            logger.info("Session closed successfully.")
        else:
            raise FailureException(message="Session is not valid or already closed.")
    
    def getEngine(self):
        if self._engine:
            return self._engine
        else:
            raise FailureException(message="Database engine is not configured. Please initialize the database first.")
        
    

    
    
   
