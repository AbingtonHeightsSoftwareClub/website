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
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    piece: Mapped[int] = mapped_column()
    position: Mapped[int] = mapped_column()
    money: Mapped[int] = mapped_column()
    password_hash: Mapped[Optional[str]] = mapped_column(String(256))

    properties = relationship(
        "Property",
        back_populates="owner",
        cascade="save-update"
    )

    def __str__(self):
        return f"Player: ID: {self.id}, Title: {self.title}, Piece: {self.piece}, Money: {self.money}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Property(db.Model):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('players.id', ondelete="SET NULL"),
        nullable=True,
        name="fk_property_user"
    )
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
    color: Mapped[str] = mapped_column(String(20))

    def __repr__(self):
        return f"Title: {self.title}, Price: {self.price}"

@login.user_loader
def load_player(id):
    return db.session.get(Player, int(id))