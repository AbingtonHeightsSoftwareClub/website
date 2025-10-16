import eventlet
from sqlalchemy import MetaData

eventlet.monkey_patch()
from extensions import socketio

from flask import Flask
import time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import pandas as pd

from flask_login import LoginManager


convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
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
    from routes.monopoly import monopoly_routes, monopoly_sockets
    from routes.auth import auth_routes
    from routes.elements import elements_routes
    from routes.chatroom import chatroom_routes
    from routes.chatroom import chatroom_sockets
    from routes.home import home_routes


    # Imports the views/webpage routes
    elements_routes.register_routes(app, db)
    home_routes.register_routes(app, db)
    auth_routes.register_routes(app, db)
    monopoly_routes.register_routes(app, db)
    chatroom_routes.register_routes(app, db)
    # Imports the socketIO connections
    monopoly_sockets.register_sockets(db)
    chatroom_sockets.register_sockets(db)

    # Database stuff
    migrate = Migrate(app, db, render_as_batch=True)

    return app
