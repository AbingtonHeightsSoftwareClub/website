# noinspection PyPackageRequirements
import os
import random
import sqlalchemy as sa
import pandas as pd
from sqlalchemy_utils import database_exists
from flask_sqlalchemy import SQLAlchemy
from models import Player, Property
from extensions import socketio
from flask_login import current_user
from flask_socketio import emit


# Routes are registered as a function, so we don't get circular imports.
# If it wasn't a function, it would get redefined multiple times, and Flask would throw errors.


def register_sockets(app, db: SQLAlchemy):
    @socketio.on("connect")
    def connect():
        # BE 100% SURE DATABASE EXISTS
        if not database_exists("sqlite:///testdb.db"):
            with app.app_context():
                db.create_all()
            data = pd.read_csv("properties.csv", index_col=0)
            for property in Property.query:
                db.session.delete(property)

            for title in data.index.values:
                property = Property(title=title,
                                    price=int(data.loc[title].iloc[0]),
                                    rent_no_set=int(data.loc[title].iloc[1]),
                                    rent_color_set=int(data.loc[title].iloc[2]),
                                    rent_1_house=int(data.loc[title].iloc[3]),
                                    rent_2_house=int(data.loc[title].iloc[4]),
                                    rent_3_house=int(data.loc[title].iloc[5]),
                                    rent_4_house=int(data.loc[title].iloc[6]),
                                    rent_hotel=int(data.loc[title].iloc[7]),
                                    building_cost=int(data.loc[title].iloc[8]),
                                    mortgage=int(data.loc[title].iloc[9]),
                                    unmortgage=int(data.loc[title].iloc[10]),
                                    position=int(data.loc[title].iloc[11]),
                                    color=data.loc[title].iloc[-1])
                db.session.add(property)
            db.session.commit()
        # If a user goes to the webpage

        # We grab all the players and properties from the database.
        players = Player.query.all()
        properties = Property.query.all()
        # Sends a message named joined. It is broadcasted to everyone.
        property_names = []
        for property_name in properties:
            property_names.append(property_name.title)
        if current_user.is_authenticated:
            emit("join",
                 {
                     "message": f"Player {current_user.title} has joined.",
                     "title": current_user.title,
                     "properties": property_names[1],
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
