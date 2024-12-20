from crypt import methods

from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy

from models import Player, Property

def register_routes(app, db: SQLAlchemy):
    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method=="GET":
            players = Player.query.all()
            return render_template('index.html', players = players)
        elif request.method=="POST":
            title = request.form.get("title")
            piece = int(request.form.get("piece"))
            position = int(request.form.get("position"))
            money = int(request.form.get("money"))

            player = Player(title=title, piece=piece, position=position, money=money)
            db.session.add(player)
            db.session.commit()
            players = Player.query.all()
            return render_template('index.html', players=players)
    @app.route("/delete/<id>", methods=["DELETE"])
    def delete(id):
        Player.query.filter(Player.id==id).delete()
        db.session.commit()
        players = Player.query.all()
        return render_template("index.html", players=players)

    @app.route("/details/<id>")
    def details(id):
        player = Player.query.filter(Player.id==id).first() # Given as list, so we need first
        return render_template("details.html", player = player)
