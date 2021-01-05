from App.Module.Config import Config, path

class ProductionConfig(Config):
    DATABASE_URI = 'sqlite:///' + path + '/Database/mydb.sqlite'
