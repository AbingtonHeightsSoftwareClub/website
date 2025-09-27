# noinspection PyPackageRequirements
import os
import random
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from models import Player, Property, Message
from extensions import socketio
from flask_login import current_user
from flask_socketio import emit
#very secure
connected = []
# Routes are registered as a function, so we don't get circular imports.
# If it wasn't a function, it would get redefined multiple times, and Flask would throw errors.

def register_sockets(db: SQLAlchemy):
    @socketio.on("connect")
    def connect(id):
        # Sends a message about who joined. It is broadcasted to everyone.
        if current_user.is_authenticated:
            connected.append(current_user.title)
            emit("chatroom-join",
                 {"message": f"{current_user.title} has joined the chatroom.", "user": current_user.title, "connected": connected},
                 broadcast=True)
            data = []
            for message in Message.query.all():
                data.append({
                         "user": message.user,
                         "message": message.text,
                     })
            emit("load-messages",
                 {"messages": data},
                     to=id,
                     broadcast=False)
            
    @socketio.on("disconnect")
    def disconnect():
        # Sends a message about who joined. It is broadcasted to everyone.
        if current_user.is_authenticated:
            connected.remove(current_user.title)
            emit("leave",
                 {"message": f"{current_user.title} has left the chatroom.", "user": current_user.title}, broadcast=True)
            
    @socketio.on("message-sent")
    def messageSent(message):
        # Sends a message sent by a user. It is broadcasted to everyone.
        if current_user.is_authenticated:
            # Send a structured payload so clients can display username and timestamp
            db.session.add(Message(user=current_user.title, text=message))
            emit("broadcast-message",
                 {
                     "user": current_user.title,
                     "message": message,
                 },
                 broadcast=True)
            db.session.commit()
            
