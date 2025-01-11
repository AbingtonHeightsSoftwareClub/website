import os

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
    @app.route("/home", methods=["GET", "POST"])
    @app.route("/", methods=["GET", "POST"])
    def creation():
        # If a user goes to the webpage
        if request.method == "GET":

            # We grab all the players and properties from the database.
            players = Player.query.all()
            properties = Property.query.all()

            # And we give the user an html file filled out with those players and properties.
            return render_template('creation.html', players=players, properties=properties)

        # If a user fills out a form
        elif request.method == "POST":


            # If they're reloading the properties
            if "property" in request.form:
                properties = Property.query.all()
                # If no properties currently exist in the database, read them from the csv file
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

                # Otherwise just grab them from the database
                else:
                    players = Player.query.all()
                    properties = Property.query.all()
                    return render_template('creation.html', players=players, properties=properties)

            # If they are making a player buy a property
            elif "buy" in request.form:
                # database.query.filter(database_name.property==something)
                # Goes through every record(row) in the database_name and if it satisfies the constraint, adds it to a list

                # In these cases, since there will only be one instance of each, first just takes it out of the list
                player = Player.query.filter(Player.title == request.form.get("buyer")).first()
                property = Property.query.filter(Property.title == request.form.get("sold")).first()
                property.player_id = player.id
                # Efficiently alters the database with the new information
                db.session.commit()
                # Even though the players didn't change, the html file needs to see the data again,
                # so we grap the data again
                players = Player.query.all()
                properties = Property.query.all()
                return render_template('creation.html', players=players, properties=properties)

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
        return render_template("creation.html", players=players, properties=properties)

    # Gives some details about a player. In the future we could add statistics, direct messaging, friending, and more.
    @app.route("/details/<id>")
    def details(id):
        player = Player.query.filter(Player.id == id).first()  # Given as list, so we need first
        return render_template("details.html", player=player)

    # This is where the game will be played. We require and account for simplified coding.
    @app.route("/monopoly")
    @login_required
    def monopoly():
        return render_template("monopoly.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # The user sends which user they are to the server as current_user. It is managed by flask_login.
        # If a user is not logged in, current_user is anonymous
        if current_user.is_authenticated:
            # Flash is a notification system. Flask automatically passes the data to the html file
            flash("Already logged in.")
            return redirect(url_for('creation'))
        # Creates the login form or grabs data (Depends on if already created or not)
        form = LoginForm()
        # If the form is correctly filled out
        if form.validate_on_submit():
            # Get the player with the title
            player = db.session.scalar(
                # sa is an alias for sqlalchemy
                sa.select(Player).where(Player.title == form.username.data))
            if player is None or not player.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))

            # Remember me autofills in the password in future logins.
            login_user(player, remember=form.remember_me.data)

            """
            Since users are often redirected to login from account protected urls, 
            they need to be redirected back to where they were from.
            
            That is done by adding /?next=/path/to/location
            to the url.
            
            <<not next_page>> is true when there is no next page(aka home)
            
            urlsplit(next_page).netloc != ""
            Means, split the url into its subcomponents, get its netloc(amazon.com, google.com) if it is not blank, 
            redirect to home. That is a cybersecurity measure. It the netloc isn't empty, it could be a hacker trying to 
            redirect other users to bad websites or inject malware into the website.
            """
            next_page = request.args.get("next")
            if not next_page or urlsplit(next_page).netloc != "":
                next_page = url_for("creation")
            return redirect(next_page)

        # Displayed when the user first visits the page.
        return render_template('login.html', form=form)

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
        # Creates form to be sent to user or grabs data (Depends on if already created or not)
        form = RegistrationForm()
        if form.validate_on_submit():
            player = Player(title=form.username.data, piece=0, position=0, money=0)
            player.set_password(form.password.data)
            db.session.add(player)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect("login")
        # Sends form data to be inserted by templating engine
        return render_template("register.html", form=form)


def register_sockets(app, db: SQLAlchemy):
    @socketio.on("connect")
    def connect():
        # Sends a message named joined. It is broadcasted to everyone.
        if current_user.is_authenticated:
            emit("join",
                 {"message": f"Player {current_user.title} has joined."}, broadcast=True)
    @socketio.test("test")
    def test():
        emit("test_complete",
             {"message": "test complete"}, broadcast=True)
