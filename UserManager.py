from User import User

def findUserById(session, id):
    return session.query(User).filter_by(id=id).first()

def findUserByName(session, name):
    return session.query(User).filter_by(name=name).first()

def validateUser(session, user):
    userFromDB = findUserByName(session, user.name)
    if (userFromDB != None and user.password == userFromDB.password):
        return userFromDB
    else:
        return None
        
def removeChatChannelIdForUser(session, userId):
    session.query(User).filter_by(id=userId).update({User.currentChatChannelId: None})
    session.commit()        
    
    
def registerNewUser(session, user): 
    if findUserByName(session, user.name) == None:
        session.add(user)
        session.commit()
        return True
    else:
        return False
        
def enterChatChannel(session, user, channel_id):
    session.query(User).filter_by(id=user.id).update({User.currentChatChannelId: channel_id})
    session.commit()