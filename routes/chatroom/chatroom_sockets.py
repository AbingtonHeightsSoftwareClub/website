# noinspection PyPackageRequirements
import os
import random
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from models import Player, Property
from extensions import socketio
from flask_login import current_user
from flask_socketio import emit

def register_sockets(db: SQLAlchemy):
    # Listen for the message event
    @socketio.on("message")
    def message(data):
        print(data)
        emit("message",
            {"message": f"{current_user.title}: {data}"}, broadcast=True)