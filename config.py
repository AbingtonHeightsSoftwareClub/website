import os


class Config:
    """
    Stores flask app config is its own place to make it neater
    """
    # An environment variable is set locally on a server
    # You can set the variable or use the default value of 'you will never guess'
    # The system admin will set a secure password.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess'

    """
    sqlite:///testdb.db means
    
    sqlite means the database uses Structured Query Language in a lightweight implementation
    :///testdb.db means the database is stored locally at test.db 
    """
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.db"
