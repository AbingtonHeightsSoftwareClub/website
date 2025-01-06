import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.db"

    # "mysql+mysqldb://softwareClub:uzxMS~6Q$p[qB}PX{/D5@softwareClub.mysql.pythonanywhere-services.com/testdb"
    # production version