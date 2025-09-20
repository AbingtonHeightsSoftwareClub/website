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

    # This is where the game will be played. We require and account for simplified coding.
    @app.route("/monopoly")
    @login_required
    def monopoly():
        return render_template("monopoly.html")

