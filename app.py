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
    login.login_view="login"
    from routes import register_routes, register_sockets
    register_routes(app, db)
    register_sockets(app, db)

    migrate = Migrate(app, db, render_as_batch=True)


    return app
