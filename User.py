import json
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey, ForeignKeyConstraint

import DbManager

class User(DbManager.declarativeBase):
    __tablename__ = "users"

    id = Column('user_id', Integer, primary_key=True)
    name = Column('username', String, unique=True)
    password = Column('password', String, nullable=False)
    currentChatChannelId = Column('current_chat_channel_id', Integer, ForeignKey('chat_channels.channel_id', use_alter=True, name='fk_node_chat_channel_id'))
    
    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __str__(self):
        return '[' + str(id) +'] ' + self.name
        
    def __add__(self, other):
        return str(self) + other
        
    def __radd__(self, other):
        return other + str(self)
  
    def toJson(self):
        return json.dumps({"id": self.id, "name": self.name})    