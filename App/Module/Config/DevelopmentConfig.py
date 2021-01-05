from App.Module.Config.Config import Config
from __init__ import path

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(path) + '/App/Database/mydb_dev.sqlite'
