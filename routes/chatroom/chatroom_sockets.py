# noinspection PyPackageRequirements
import os
import random
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from models import Player, Property, Message, ActiveUsers, Room
from extensions import socketio
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

# Routes are registered as a function, so we don't get circular imports.
# If it wasn't a function, it would get redefined multiple times, and Flask would throw errors.

def register_sockets(db: SQLAlchemy):
    @socketio.on("connect")
    def connect(id):
        # Sends a message about who joined. It is broadcasted to everyone.
        if current_user.is_authenticated:
            join_room(current_user.room)
            # If the user isn't already in the database, add the user to the database of Active Users
            if len(ActiveUsers.query.filter_by(id=current_user.id, room=current_user.room).all())==0:
                db.session.add(ActiveUsers(id=current_user.id, title=current_user.title, room=current_user.room))
                db.session.commit()
            
            # Send the list of every user connected to the chat room and their id
            emit("join",
                 {"message": f"{current_user.title} has joined the chatroom.", "users": [{"id": user.id, "title": user.title} for user in ActiveUsers.query.filter_by(room=current_user.room).all()]},
                 broadcast=True, to=current_user.room)
            data = []
            print(f"ROOM TITLE: {Room.query.first().title}")
            print(f"CURRENT_USER.ROOM: {current_user.room}")
            for message in Room.query.filter_by(title=current_user.room).first().messages:
                data.append({
                         "user": message.user,
                         "message": message.text,
                         "time": message.time,
                     })
            emit("load-messages",
                 {"messages": data},
                     to=id,
                     broadcast=False)
            
    @socketio.on("disconnect")
    def disconnect():
        # Sends a message about who joined. It is broadcasted to everyone.
        if current_user.is_authenticated:
            leave_room(current_user.room)
            print(current_user.id)
            ActiveUsers.query.filter_by(id=current_user.id).delete()
            db.session.commit()

            emit("leave",
                 {"message": f"{current_user.title} has left the chatroom.", "id": current_user.id},
                 broadcast=True, to=current_user.room)

    @socketio.on("private-room-creation")
    def private_room_creation(password, room_id):
        # Get the room
        room = Room.query.filter_by(title=current_user.room).first()
        # set the title
        room.title = room_id
        # Set the password
        room.password = password
        print(f"password: {room.password}")
        db.session.commit()

    @socketio.on("room-password-check")
    def room_password_check(room_id, password_to_check):
        room = Room.query.filter_by(title=room_id).first()
        if room.password == password_to_check:
            emit("room-password-result", {"password_matches": True, "room_id": room_id}, to=current_user.room)
        else:
            emit("room-password-result", {"password_matches": False, "room_id": room_id}, to=current_user.room)

    @socketio.on("message-sent")
    def message_sent(message, time):
        # Sends a message sent by a user. It is broadcasted to everyone.
        if current_user.is_authenticated:
            # Send a structured payload so clients can display username and timestamp
            db.session.add(Message(user=current_user.title, text=message, time=time, room=current_user.room, temp_room=Room.query.filter_by(title=current_user.room).first()))
            emit("broadcast-message",
                 {
                     "user": current_user.title,
                     "message": message,
                     "time" : time
                 },
                 broadcast=True, to=current_user.room)
            db.session.commit()

    @socketio.on("typing-event")
    def typingEvent():
        # Notifies everyone that a certain user is typing
        if current_user.is_authenticated:
            emit("typing-event", {
                "user": current_user.title
            },
                 broadcast=True, include_self=False, to=current_user.room)

    @socketio.on("typing-stopped")
    def typingStopped():
        if current_user.is_authenticated:
            emit("typing-stopped", {
                "user": current_user.title
            },
                 broadcast=True, include_self=False, to=current_user.room)



            
