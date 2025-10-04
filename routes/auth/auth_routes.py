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


def register_routes(app, db: SQLAlchemy):
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # The user sends which user they are to the server as current_user. It is managed by flask_login.
        # If a user is not logged in, current_user is anonymous
        if current_user.is_authenticated:
            # Flash is a notification system. Flask automatically passes the data to the html file
            flash("Already logged in.")
            return redirect(url_for('home'))
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
                next_page = url_for("home")
            return redirect(next_page)

        # Displayed when the user first visits the page.
        return render_template('login.html', form=form)

    @app.route("/logout", methods=["GET", "POST"])
    def logout():
        if not current_user.is_authenticated:
            flash("Not logged in.")
            return redirect(url_for("home"))
        logout_user()
        return redirect(url_for("home"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            flash("Already logged in.")
            return redirect(url_for("home"))
        # Creates form to be sent to user or grabs data (Depends on if already created or not)
        form = RegistrationForm()
        if form.validate_on_submit():
            player = Player(title=form.username.data, piece=0, position=0, money=0, room=None)
            player.set_password(form.password.data)
            db.session.add(player)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect("login")
        # Sends form data to be inserted by templating engine
        return render_template("register.html", form=form)