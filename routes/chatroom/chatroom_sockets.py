# noinspection PyPackageRequirements
import os
import random
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from models import Player, Property
from extensions import socketio
from flask_login import current_user
from flask_socketio import emit


# Routes are registered as a function, so we don't get circular imports.
# If it wasn't a function, it would get redefined multiple times, and Flask would throw errors.

def register_sockets(db: SQLAlchemy):
    @socketio.on("connect")
    def connect():
        # Sends a message about who joined. It is broadcasted to everyone.
        if current_user.is_authenticated:
            emit("join",
                 {"message": f"{current_user.title} has joined the chatroom."}, broadcast=True)
    @socketio.on("message-sent")
    def messageSent(message):
        # Sends a message sent by a user. It is broadcasted to everyone.
        if current_user.is_authenticated:
            # Send a structured payload so clients can display username and timestamp
            emit("broadcast-message",
                 {
                     "user": current_user.title,
                     "message": message,
                 },
                 broadcast=True)