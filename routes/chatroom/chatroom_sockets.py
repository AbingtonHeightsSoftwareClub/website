# noinspection PyPackageRequirements
import os
import random
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from models import Player, Property, Message
from extensions import socketio
from flask_login import current_user
from flask_socketio import emit


# Routes are registered as a function, so we don't get circular imports.
# If it wasn't a function, it would get redefined multiple times, and Flask would throw errors.

def register_sockets(db: SQLAlchemy):
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
    
    #Loads all messages saved in the db to the chatroom, only loads to user who sent "load-messages"
    @socketio.on("load-messages")
    def loadMessages(id):
        if current_user.is_authenticated:
            for message in Message.query:
                emit("broadcast-message",
                 {
                     "user": message.user,
                     "message": message.text,
                 },
                 to=id,
                 broadcast=False)