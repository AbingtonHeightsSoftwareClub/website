import eventlet

eventlet.monkey_patch()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import pandas as pd
from extensions import socketio
from flask_login import LoginManager



db = SQLAlchemy()
login = LoginManager()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    db.init_app(app)
    socketio.init_app(app)
    login.init_app(app)

    # Login protected views will force not logged-in users to /login
    login.login_view = "login"

    # Importing like this stops circular imports
    from routes import register_routes, register_sockets
    # Imports the views/webpage routes
    register_routes(app, db)
    # Imports the socketIO connections
    register_sockets(app, db)

    # Database stuff
    migrate = Migrate(app, db, render_as_batch=True)

    return app
