import psycopg2
import json
from LoginForm import LoginForm
from RegistrationForm import RegistrationForm
from CreateChatChannelForm import CreateChatChannelForm
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, fresh_login_required, login_required, LoginManager
import UserManager
from ChatChannelMessage import ChatChannelMessage
from User import User
from DbManager import DbManager
from ChatChannel import ChatChannel
import ChatChannelManager
from flask import jsonify
from sqlalchemy.orm import aliased, joinedload


DEBUG = True
SECRET_KEY = 'asdfaf3q4534tegsdfgsdfgsd'

app = Flask(__name__)
app.config.from_object(__name__)
loginManager = LoginManager()
loginManager.init_app(app)

dbManager = DbManager();
dbManager.createTables();
sessionMaker = dbManager.createSessionMaker()
session = sessionMaker()

@loginManager.user_loader
def load_user(userid):
    return UserManager.findUserById(session, userid)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('chatChannels'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data == form.passwordConfirmation.data:
            user = User(form.username.data, form.password.data)
            if UserManager.registerNewUser(session, user):
                return redirect(request.args.get("next") or url_for("login"))
            else:
                flash('This username is already in use')
        else:
            flash('Passwords do not match')
    return render_template("register.html", form=form)    

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('chatChannels'))

    form = LoginForm()
    if form.validate_on_submit():
        validUser = UserManager.validateUser(session, User(form.username.data, form.password.data))
        if (validUser != None):
            login_user(validUser)
            return redirect(request.args.get("next") or url_for("chatChannels"))
        else:
            flash('Incorrect username or password')
    return render_template("login.html", form=form)

@app.route("/chat_channel/<int:channel_id>")
@login_required
def chatChannel(channel_id):
    UserManager.enterChatChannel(session, current_user, channel_id)
    return render_template("chat_channel.html", channel_id = channel_id)    
    
@app.route("/chat_channel/<int:channel_id>/leave")
@login_required
def leaveChatChannel(channel_id):
    UserManager.removeChatChannelIdForUser(session, current_user.id)
    return redirect(url_for('chatChannels'))
    
@app.route("/chat_channel/<int:channel_id>/status", methods=["GET", "POST"])
@login_required
def chatChannelStatus(channel_id):
    messages = session.query(ChatChannelMessage, User).join(User).order_by(ChatChannelMessage.timestamp.desc()).limit(10).all()
    messagesJson = []
    for message, user in messages:
        messagesJson.append('{"message": "'+message.message+'", "username": "'+user.name+'", "timestamp": "'+ message.timestamp.strftime('%H:%m:%S') +'"}')
    messagesJson.reverse()
    
    users = session.query(User).filter_by(currentChatChannelId=channel_id).all()
    usersJson=[e.toJson() for e in users]
    
    return jsonify(users=usersJson, messages=messagesJson)
    
@app.route("/chat_channel/<int:channel_id>/post_message", methods=["GET", "POST"])
@login_required
def chatChannelPostMessage(channel_id):
    message = ChatChannelMessage(user_id = current_user.id, message = str(request.form['message']), channel_id = channel_id)
    session.add(message)
    session.commit()
    return ''
    
@app.route("/chat_channels")
@login_required
def chatChannels():
    channels = session.query(ChatChannel)
    return render_template("chat_channels.html", channels=channels)
    
@app.route("/chat_channels_search", methods=["GET", "POST"])
@login_required
def chatChannelsSearch():
    channels = ChatChannelManager.findChannels(session, str(request.args['chat_channel_name']))
    return render_template("chat_channels.html", channels=channels)
    
@app.route("/create_chat_channel", methods=["GET", "POST"])
@login_required
def createChatChannel():
    form = CreateChatChannelForm()
    if form.validate_on_submit():
        if ChatChannelManager.createNewChatChannel(session, ChatChannel(form.name.data, form.description.data)):
            return redirect(request.args.get("next") or url_for("chatChannels"))
        else:
            flash('Channel with such name already exists')
    return render_template("create_chat_channel.html", form=form) 
    
@app.route("/logout")
@login_required
def logout():
    UserManager.removeChatChannelIdForUser(session, current_user.id)
    logout_user()
    return redirect('home')    

@app.route("/")    
@app.route("/home")
def home():
    return render_template("home.html")

@app.teardown_appcontext
def shutdown_session(exception=None):
    if session is not None:
        session.close()    
    
if __name__ == '__main__':
    app.run()