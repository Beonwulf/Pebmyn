from dataclasses import dataclass
from urllib.parse import urlparse
from flask import Flask, request
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
# from flask.ext.principal import Principal
from flask_wtf.csrf import CSRFProtect
from App.Module.Config.DevelopmentConfig import DevelopmentConfig
from App.Database.db import db
from App.Database.Models.User import User, Role
from __init__ import path


@dataclass()
class MyApp:
    my_app: Flask = None
    login_manager: LoginManager = None
    user_datastore: SQLAlchemyUserDatastore = None
    security: Security = None
    csrf: CSRFProtect = None
    init: bool = False


    def __init__(self):
        self.my_app = Flask(__name__, static_url_path=None)
        self.init_app()

    def getApp(self):
        return self.my_app


    def getSecurity(self):
        if not self.init:
            raise myAppError('[myApp:getSecurity] call myApp::init_app first!')
        return self.security
    

    def registerBlueprint(self, blueprint):
        if not self.init:
            raise myAppError('[myApp:registerBlueprint] call myApp::init_app first!')
        self.my_app.register_blueprint(blueprint)
    

    def registerFormLogin(self, form):
        self.security.login_form = form


    def init_app(self):
        self.create_app()
        self.configure_app()
        self.init_login_manager()
        self.configure_security()
        db.init_app(self.my_app)
        self.check_db()
        self.init = True


    def create_app(self):
        # Principal(self.my_app)
        self.security = Security(self.my_app)
        self.login_manager = LoginManager()
        self.csrf = CSRFProtect()
        self.csrf.init_app(self.my_app)
        

    def configure_app(self):
        self.my_app.config.from_object(DevelopmentConfig())
        self.my_app.static_url_path='/web/static'
        self.my_app.static_folder= self.my_app.root_path + self.my_app.static_url_path
        self.my_app.static_folder= str(path) + self.my_app.static_url_path
        self.my_app.template_folder=path / 'web/templates'


    def init_login_manager(self):
        # Setup Flask-Security
        self.user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        self.login_manager.init_app(self.my_app)
        @self.login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)
    
    def configure_security(self):
        self.security.init_app(app=self.my_app,datastore=self.user_datastore, register_blueprint=True)


    def check_db(self):
        #self.build_db()
        pass

    def build_db(self):
        db.drop_all()
        db.create_all()
        from flask_security.utils import encrypt_password
        with self.my_app.app_context():
            user_role = Role(name='user')
            customer_role = Role(name='Customer')
            reseller_role = Role(name='Reseller')
            super_user_role = Role(name='superuser')
            admin_user_role = Role(name='admin')
            db.session.add(admin_user_role)
            db.session.add(super_user_role)
            db.session.add(customer_role)
            db.session.add(reseller_role)
            db.session.add(user_role)
            db.session.commit()
            #test_user = self.user_datastore.create_user(
            #    name='Admin',
            #    email='admin@admin.sz',
            #    password=encrypt_password('admin'),
            #    roles=[user_role, customer_role, reseller_role, super_user_role, admin_user_role]
            #)
            #db.session.commit()
            self.security.datastore.create_user(
                username='Admin',
                email='admin@admin.sz',
                password=encrypt_password('admin'),
                roles=[user_role, customer_role, reseller_role, super_user_role, admin_user_role]
            )
            self.security.datastore.commit()
            #db.session.add()
            return

    def run(self):
        # ToDo SSL - if file exists cert.pem
        # app.run(port=cfg.get_port(), debug=cfg.get_debug(), ssl_context=('cert.pem', 'key.pem'))
        # self.my_app.run(port=cfg.get_port(), debug=cfg.get_debug(), ssl_context='adhoc')
        # self.my_app.run(port=2402, debug=True, ssl_context='adhoc')
        self.my_app.run(debug=True, ssl_context='adhoc')


class myAppError(LookupError):
    ''''''


#app = MyApp()
#app.init_app()
