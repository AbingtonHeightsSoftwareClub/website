import os
from typing import List

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


def register_routes(app, db: SQLAlchemy):
    @app.route("/home", methods=["GET", "POST"])
    @app.route("/", methods=["GET", "POST"])
    def creation():
        if request.method == "GET":
            players = Player.query.all()
            properties = Property.query.all()
            return render_template('creation.html', players=players, properties=properties)
        elif request.method == "POST":
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
                return render_template('creation.html', players=players, properties=properties)
            elif "property" in request.form:
                properties = Property.query.all()
                if len(properties) == 0:
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
                    return render_template('creation.html', players=players, properties=properties)
                else:
                    players = Player.query.all()
                    properties = Property.query.all()
                    return render_template('creation.html', players=players, properties=properties)

            elif "buy" in request.form:
                player = Player.query.filter(Player.title == request.form.get("buyer")).first()
                property = Property.query.filter(Property.title == request.form.get("sold")).first()
                property.user_id = player.id
                db.session.commit()
                players = Player.query.all()
                properties = Property.query.all()
                return render_template('creation.html', players=players, properties=properties)

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'img/softwareClubLogoPlain.png')

    @app.route("/delete_player/<id>", methods=["DELETE"])
    def delete_player(id):
        player = Player.query.filter(Player.id == id).first()
        db.session.delete(player)
        keys = Property.query.filter(Property.user_id == id).all()
        for key in keys:
            key = None
        db.session.commit()
        players = Player.query.all()
        print(len(players))
        properties = Property.query.all()
        return render_template("creation.html", players=players, properties=properties)

    @app.route("/delete_property/", methods=["DELETE"])
    def delete_property():
        db.session.query(Property).delete()

        db.session.commit()
        players = Player.query.all()
        properties = Property.query.all()
        return render_template("creation.html", players=players, properties=properties)

    @app.route("/details/<id>")
    def details(id):
        player = Player.query.filter(Player.id == id).first()  # Given as list, so we need first
        return render_template("details.html", player=player)

    @app.route("/monopoly")
    @login_required
    def monopoly():
        return render_template("monopoly.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            flash("Already logged in.")
            return redirect(url_for('creation'))
        form = LoginForm()
        if form.validate_on_submit():
            player = db.session.scalar(
                sa.select(Player).where(Player.title == form.username.data))
            if player is None or not player.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(player, remember=form.remember_me.data)
            next_page = request.args.get("next")
            if not next_page or urlsplit(next_page).netloc != "":
                next_page = url_for("creation")
            """
        If the login URL does not have a next argument, then the user is redirected to the index page.
    
        If the login URL includes a next argument that is set to a relative path (or in other words, 
    a URL without the domain portion), then the user is redirected to that URL.
    
        If the login URL includes a next argument that is set to a full URL that includes a domain name, 
    then this URL is ignored, and the user is redirected to the index page (cyber security).
            """
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        if not current_user.is_authenticated:
            flash("Not logged in.")
            return redirect(url_for("creation"))
        logout_user()
        return redirect(url_for("creation"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            flash("Already logged in.")
            return redirect(url_for("creation"))
        form = RegistrationForm()
        if form.validate_on_submit():
            player = Player(title=form.username.data, piece=0, position=0, money=0)
            player.set_password(form.password.data)
            db.session.add(player)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect("login")
        return render_template("register.html", form=form)


def register_sockets(app, db: SQLAlchemy):
    @socketio.on("connect")
    def connect():
        if current_user.is_authenticated:
            emit("join",
                 {"message": f"Player {current_user.title} has joined."}, broadcast=True)
