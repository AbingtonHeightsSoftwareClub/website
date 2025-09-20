# noinspection PyPackageRequirements
import os
import random

import sqlalchemy as sa
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

from forms import LoginForm, RegistrationForm
from models import Player, Property
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

    # Home and / are used interchangeably, so we led both of them point to the current home page.
    # We can change it to a more official home page in the future.
    @app.route("/home")
    @app.route("/")
    def home():
        # If a user goes to the webpage

        # We grab all the players and properties from the database.
        players = Player.query.all()
        properties = Property.query.all()

        # And we give the user an html file filled out with those players and properties.
        return render_template('home.html', players=players, properties=properties)

    # Fancy name for website logo in the tab
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'img/softwareClubLogoPlain.png')

    # This deletes a player from the database. Since it does not have a GET method, it is not a visible webpage.
    @app.route("/delete_player/<id>", methods=["DELETE"])
    def delete_player(id):
        player = Player.query.filter(Player.id == id).first()
        db.session.delete(player)
        db.session.commit()
        players = Player.query.all()
        properties = Property.query.all()
        return render_template("home.html", players=players, properties=properties)

    # Gives some details about a player. In the future we could add statistics, direct messaging, friending, and more.
    @app.route("/details/<id>")
    def details(id):
        player = Player.query.filter(Player.id == id).first()  # Given as list, so we need first
        return render_template("details.html", player=player)

