# noinspection PyPackageRequirements
import os
import random

import sqlalchemy as sa
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

from forms import LoginForm, RegistrationForm
from models import Player, Property, Message, ActiveUsers, Room
from flask import send_from_directory
from extensions import socketio
from flask_login import current_user, login_user, logout_user, login_required

from urllib.parse import urlsplit
from flask_socketio import emit


# Routes are registered as a function, so we don't get circular imports.
# If it wasn't a function, it would get redefined multiple times, and Flask would throw errors.

def register_routes(app, db: SQLAlchemy):
    """
    @app.route("/path/to/location", methods=[methods])

    This means the function below it is run when ahsoftware.club/path/to/location is gone to by the user

    Methods lists the methods that the webpage accepts
    Read here to learn them all https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

    The most common are GET and POST
    When a user wants a webpage, they GET it from the server.
    They can fill out a form and send data by POST office to the server.

    When you see
    @app.route("path")
    @app.route("other_path")

    It means both of those paths point to the same function/webpage.
    """

    # This is where the game will be played. We require and account for simplified coding.
    @app.route("/chatroom")
    @login_required
    def chatroom():
        # If they don't have a room, make them choose one
        if current_user.room is None:
            return redirect(url_for("choose_chatroom", room="choose"))
        # If they have a room, serve it to them
        return render_template("chatroom/chatroom.html", room=current_user.room)

    """
    If someone enters nothing as the new room they want, they get redirected here.
    """
    @app.route("/chatroom/choose_chatroom/")
    @login_required
    def empty_choose_chatroom():
        return redirect(url_for("choose_chatroom", room="choose"))

    # Dynamic URL for the choose screen
    @app.route("/chatroom/choose_chatroom/<room>", methods=["GET", "POST"])
    @login_required
    def choose_chatroom(room: str):
        # if they don't have a room
        if room == "choose":
            # Define all rooms and all users in those rooms every time so that no user is missed.
            active_users: dict = dict()
            rooms: set = set()
            # Contains a set of all password protected rooms
            private_rooms: set = set()
            # Add all the private rooms to their own set
            for room in Room.query.all():
                if room.password is not None:
                    private_rooms.add(int(room.title))
            # For every active user ever
            for user in ActiveUsers.query.all():
                # Add every possible room (it's a set so no duplicates)
                rooms.add(user.room)
                # Create a dictionary entry that contains a list of every active user in room n
                active_users[user.room] = [active_user.title for active_user in ActiveUsers.query.filter_by(room=user.room).all()]


            # If a room has messages in it, we want to be able to go to it and see what people sent. So, we need to list rooms that have messages in them.
            for message in Message.query.all():
                rooms.add(message.room)


            return render_template(
                  "chatroom/choose_chatroom.html",
                                   rooms=rooms,
                                   active_users=active_users,
                                   private_rooms=private_rooms
            )

        else:
            try:
                room = int(room)

            except ValueError:
                print("Error")

                return redirect(url_for("choose_chatroom", room="choose"))

            current_user.room = int(room)
            if len(list(Room.query.filter_by(title=current_user.room)))==0:
                test_rooms = Room(title=room)
                db.session.add(test_rooms)
            db.session.commit()
            return redirect(url_for("chatroom"))


    # Deletes the chat db, bandaid solution rn but we'll change it later
    @app.route("/delete_chats")
    @login_required
    def delete_chats():
        for message in Message.query:
            db.session.delete(message)
        db.session.commit()
        return render_template("chatroom/chatroom.html")
