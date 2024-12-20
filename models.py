from sqlalchemy.orm import relationship

from app import db
import pandas as pd


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, db.Sequence('player_id_seq'), primary_key=True)
    title = db.Column(db.String(50))
    piece = db.Column(db.Integer)
    position = db.Column(db.Integer)
    money = db.Column(db.Integer)
    # The player owns a list of properties
    properties = relationship("Property",
                              back_populates="player")  # Backpopulates to other relationship column/variable. Not class object name.

    def __repr__(self):
        return f"Player: ID: {self.id}, Title: {self.title}, Piece: {self.piece}, Money: {self.money}"


class Property(db.Model):
    __tablename__ = "properties"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("players.id"))

    price = db.Column(db.Integer)
    rent_no_set = db.Column(db.Integer)
    rent_color_set = db.Column(db.Integer)
    rent_1_house = db.Column(db.Integer)
    rent_2_house = db.Column(db.Integer)
    rent_3_house = db.Column(db.Integer)
    rent_4_house = db.Column(db.Integer)
    rent_hotel = db.Column(db.Integer)
    building_cost = db.Column(db.Integer)
    mortgage = db.Column(db.Integer)
    unmortgage = db.Column(db.Integer)
    color = db.Column(db.String(10))

    player = relationship("Player",
                          back_populates="properties")  # Must be same as what the other back_populates is called

    def __repr__(self):
        return f"Title: {self.title}, Price: {self.price}"

#
# def add_player(session: Session, title: str, piece: int, position: int, money: int):
#     session.add(Player(title=title, piece=piece, position=position, money=money))
#
# def add_properties(session:Session, in_filename: str):
#     data = pd.read_csv(in_filename, index_col=0)
#     for title in data.index.values:
#         #values = [int(x) for x in data.loc[title].iloc[0: -1]]
#         session.add(Property(title = title,
#                              price=int(data.loc[title][0]),
#                              rent_no_set=int(data.loc[title][1]),
#                              rent_color_set=int(data.loc[title][2]),
#                              rent_1_house=int(data.loc[title][3]),
#                              rent_2_house=int(data.loc[title][4]),
#                              rent_3_house=int(data.loc[title][5]),
#                              rent_4_house=int(data.loc[title][6]),
#                              rent_hotel=int(data.loc[title][7]),
#                              building_cost=int(data.loc[title][8]),
#                              mortgage=int(data.loc[title][9]),
#                              unmortgage=int(data.loc[title][10]),
#                              color=data.loc[title].iloc[-1]))
#
#
#
#
# if __name__=="__main__":
#     add_player(session, "Alice", 10, 10, 10)
#     add_properties(session, "properties.csv")
#     session.commit()
#
#
#     name = "hello"
#     for prop in session.query(Property).all():
#         print(prop)
