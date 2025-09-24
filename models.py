import eventlet
eventlet.monkey_patch()

from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Player(UserMixin, db.Model):
    __tablename__ = "players"
    # column_name: Mapped[data_type_of_column] = column object with configurations
    # Primary key means it is the index column
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    piece: Mapped[int] = mapped_column()
    position: Mapped[int] = mapped_column()
    money: Mapped[int] = mapped_column()

    # Secure way to store passwords. If you want to know more look it up.
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))

    # It establishes the relationship between Player and Properties.
    # If a player is deleted, the property owner id is set to null
    properties = relationship(
        "Property",
        back_populates="owner",
        cascade="save-update"
    )

    # The value of str(Player) is defined here. Useful for printing/debugging.
    def __str__(self):
        return f"Player: ID: {self.id}, Title: {self.title}, Piece: {self.piece}, Money: {self.money}"

    # Sets the password as the hash of the given password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Hashes the password and checks it to the stored hash. If true, login is correct.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Property(db.Model):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    # This stores the id of the player that owns it. <<ondelete="SET NULL">> means if
    # the owner is deleted, the id is set to null.
    # The name is used in the migration service. You do not need to know what it does.
    player_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('players.id', ondelete="SET NULL"),
        nullable=True,
        name="fk_property_user"
    )

    # Tells SQLalchemy that it is owned by the player
    owner = relationship("Player", back_populates="properties")

    price: Mapped[int] = mapped_column()
    rent_no_set: Mapped[int] = mapped_column()
    rent_color_set: Mapped[int] = mapped_column()
    rent_1_house: Mapped[int] = mapped_column()
    rent_2_house: Mapped[int] = mapped_column()
    rent_3_house: Mapped[int] = mapped_column()
    rent_4_house: Mapped[int] = mapped_column()
    rent_hotel: Mapped[int] = mapped_column()
    building_cost: Mapped[int] = mapped_column()
    mortgage: Mapped[int] = mapped_column()
    unmortgage: Mapped[int] = mapped_column()
    position: Mapped[int] = mapped_column()
    # String(20) means the color has to be less than 20 characters long
    color: Mapped[str] = mapped_column(String(20))

    # The value of str(Property) is defined here. Useful for printing/debugging.
    def __str__(self):
        return f"Title: {self.title}, Price: {self.price}, Position {self.position}"


# This is necessary for the login system.
@login.user_loader
def load_player(id):
    return db.session.get(Player, int(id))
