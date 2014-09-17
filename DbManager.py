from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

import Settings

declarativeBase = declarative_base()

class DbManager:
    
    def __init__(self):
        self.engine = create_engine(Settings.SQLALCHEMY_DATABASE_URI)
        self.declarativeBase = declarativeBase
    
    def getEngine(self):
        return self.engine
    
    def createSessionMaker(self):
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        declarativeBase.query = session.query_property()
        return session
    
    def createTables(self):
        self.declarativeBase.metadata.create_all(self.engine)