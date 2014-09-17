
from ChatChannel import ChatChannel

def createNewChatChannel(session, chatChannel):
    chatChannelFromDb = session.query(ChatChannel).filter_by(name=chatChannel.name).first()
    if chatChannelFromDb == None:
        session.add(chatChannel)
        session.commit()
        return True
    else:
        return False
        
def findChannels(session, likeName):
    return session.query(ChatChannel).filter(ChatChannel.name.like(likeName + '%'))
