from App.Routes.auth import r_auth
from App.Routes.my_profile import my_profile
from App.Routes.main import r_main
from App.Routes.hosting_services import r_hostingservices
from App.Routes.server_managetment import r_servermanagment


def registerRoutes(app):
    app.registerBlueprint(r_auth)
    app.registerBlueprint(my_profile)
    app.registerBlueprint(r_main)
    app.registerBlueprint(r_hostingservices)
    app.registerBlueprint(r_servermanagment)
