import os
import json
import base64
import pathlib


class Settings():
    cfg = None
    cfgPath = None
    cfgFile = None

    def __init__(self):
        self.cfg = {}
        
        self.cfgPath = pathlib.Path(__file__).parent.absolute()
        self.cfgFile = self.cfgPath / 'config.json'
        self.load()
    
    def get(self):
        return self.cfg

    def load(self):
        if not os.path.isfile(self.cfgFile):
            self.default()
            self.save()
        else:
            with open(self.cfgFile) as json_file:
                self.cfg = json.load(json_file)


    def save(self):
        with open(self.cfgFile, 'w') as outfile:
            json.dump(self.cfg, outfile)
        #pass

    def default(self):
        from __init__ import path
        self.cfg['app'] = {
            'path': str(path),
            'key': base64.b64encode(bytearray(os.urandom(24))).decode(),
            'server_name': 'localhost',
            #'server_port': 2402,
            'threaded': True,
            'csrf': True,
            'track_modification': True
        }
        self.cfg['SECURITY'] = {
            # Flask-Security config
            #'URL_PREFIX': '/admin',
            'URL_PREFIX': '/',
            'PASSWORD_HASH': 'pbkdf2_sha512',
            'PASSWORD_SALT': base64.b64encode(bytearray(os.urandom(31))).decode(),
            # Flask-Security URLs, overridden because they don't put a / at the end
            'LOGIN_URL': '/login/',
            'LOGOUT_URL': '/logout/',
            'REGISTER_URL': '/register/',
            # Flask-Security features
            'REGISTERABLE': True,
            'SEND_REGISTER_EMAIL': False,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
    
    def applicationPort(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [ env['SERVER_PORT'] ]

    def applicationMode(self, environ, start_response):
        status = '200 OK'

        if not environ['mod_wsgi.process_group']:
            output = u'EMBEDDED'
        else:
            output = u'DAEMON'

        response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(output)))]

        start_response(status, response_headers)

        return [output.encode('UTF-8')]


config = Settings()
cfg = config.get()



class Config(object):
    SECRET_KEY = cfg['app']['key']
    #FLASK_SERVER_PORT = cfg['app']['server_port']
    FLASK_THREADED = cfg['app']['threaded']
    FLASK_DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = cfg['app']['csrf']
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = cfg['SECURITY']['SQLALCHEMY_TRACK_MODIFICATIONS']
    SECURITY_PASSWORD_HASH = cfg['SECURITY']['PASSWORD_HASH']
    SECURITY_PASSWORD_SALT = cfg['SECURITY']['PASSWORD_SALT']
