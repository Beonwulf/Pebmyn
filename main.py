from App.myApp import MyApp
from App.Routes import registerRoutes
from urllib.parse import urlparse
from flask import Flask, request
from flask_menu import Menu, register_menu
from flask_menu import current_menu


class Main:
    def __init__(self, app):
        self.app = app
        self.routes()

    
    def routes(self):
        registerRoutes(self.app)


    def run(self):
        self.app.run()


ma = MyApp()
main = Main(ma)
app = ma.getApp()
Menu(app=app)


# Create a user to test with
@app.before_first_request
def create_test_user():
    ma.build_db()


if __name__ == "__main__":
    main.run()
