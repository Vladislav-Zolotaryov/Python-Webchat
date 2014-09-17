from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import DbManager

class ChatChannel(DbManager.declarativeBase):
    __tablename__ = "chat_channels"

    id = Column('channel_id', Integer, primary_key=True)
    name = Column('name', String, unique=True)
    description = Column('description', String)

    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return self.name
        
    def __add__(self, other):
        return str(self) + other
        
    def __radd__(self, other):
        return other + str(self)