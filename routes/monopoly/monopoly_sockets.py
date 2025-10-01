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
        # Sends a message named joined. It is broadcasted to everyone.

        if current_user.is_authenticated:
            emit("join",
                 {
                     "message": f"Player {current_user.title} has joined.",
                     "title": current_user.title,
                     "properties": Property.query.all()
                 },
                 broadcast=True)

    @socketio.on("roll")
    def roll():
        old_position = current_user.position
        roll = random.randint(1, 6) + random.randint(1, 6)
        current_user.position = (old_position + roll) % 41
        if current_user.position == 0:
            current_user.position = 1
        print(current_user.position)
        db.session.commit()
        emit("rolled",
             {"user": current_user.title, "current_position": current_user.position, "old_position": old_position,
              "roll": roll}, broadcast=True)
