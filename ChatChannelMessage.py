import json
import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship, backref

import DbManager
from User import User

class ChatChannelMessage(DbManager.declarativeBase):
    __tablename__ = "chat_channel_messages"

    id = Column('message_id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.user_id', use_alter=True, name='fk_node_user_id'))
    user = relationship(User, backref='chat_channel_messages')
    channel_id = Column('chat_channel_id', Integer, ForeignKey('chat_channels.channel_id', use_alter=True, name='fk_node_chat_channel_id'))
    message = Column('message', String, nullable=False)
    timestamp = Column('timestamp', DateTime, default=datetime.datetime.utcnow)
    
    def __init__(self, user_id, channel_id, message):
        self.user_id = user_id
        self.channel_id = channel_id
        self.message = message
        
    def toJson(self):
        return json.dumps({"message": self.message, "timestamp": str( self.timestamp )})            