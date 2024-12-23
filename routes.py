from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from models import Player, Property

def register_routes(app, db: SQLAlchemy):
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method=="GET":
            players = Player.query.all()
            properties = Property.query.all()
            return render_template('index.html', players = players, properties=properties)
        elif request.method=="POST":
            if "player" in request.form:
                title = request.form.get("title")
                piece = int(request.form.get("piece"))
                position = int(request.form.get("position"))
                money = int(request.form.get("money"))

                player = Player(title=title, piece=piece, position=position, money=money)
                db.session.add(player)
                db.session.commit()
                players = Player.query.all()
                properties = Property.query.all()
                return render_template('index.html', players=players, properties=properties)
            elif "property" in request.form:
                properties = Property.query.all()
                if len(properties)==0:
                    data = pd.read_csv("properties.csv", index_col=0)
                    for title in data.index.values:
                        db.session.add(Property(title=title,
                                                       price=int(data.loc[title][0]),
                                                       rent_no_set=int(data.loc[title][1]),
                                                       rent_color_set=int(data.loc[title][2]),
                                                       rent_1_house=int(data.loc[title][3]),
                                                       rent_2_house=int(data.loc[title][4]),
                                                       rent_3_house=int(data.loc[title][5]),
                                                       rent_4_house=int(data.loc[title][6]),
                                                       rent_hotel=int(data.loc[title][7]),
                                                       building_cost=int(data.loc[title][8]),
                                                       mortgage=int(data.loc[title][9]),
                                                       unmortgage=int(data.loc[title][10]),
                                                       color=data.loc[title].iloc[-1]))
                    db.session.commit()
                    players = Player.query.all()
                    properties = Property.query.all()
                    return render_template('index.html', players=players, properties=properties)
                else:
                    players = Player.query.all()
                    properties = Property.query.all()
                    return render_template('index.html', players=players, properties=properties)

            elif "buy" in request.form:
                player = Player.query.filter(Player.title==request.form.get("buyer")).first()
                property = Property.query.filter(Property.title==request.form.get("sold")).first()
                property.user_id=player.id
                db.session.commit()
                players = Player.query.all()
                properties = Property.query.all()
                return render_template('index.html', players=players, properties=properties)




    @app.route("/delete_player/<id>", methods=["DELETE"])
    def delete_player(id):
        player = Player.query.filter(Player.id==id).first()
        db.session.delete(player)
        db.session.commit()
        print("Test")
        players = Player.query.all()
        print(len(players))
        properties = Property.query.all()
        return render_template("index.html", players=players, properties=properties)

    @app.route("/delete_property/", methods=["DELETE"])
    def delete_property():
        db.session.query(Property).delete()
        db.session.commit()
        players = Player.query.all()
        properties = Property.query.all()
        return render_template("index.html", players=players, properties=properties)

    @app.route("/details/<id>")
    def details(id):
        player = Player.query.filter(Player.id==id).first() # Given as list, so we need first
        return render_template("details.html", player = player)

    @app.route("/monopoly")
    def monopoly():
        return render_template("monopoly.html")

