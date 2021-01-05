import functools


class MySideBar:


    def __init__(self):
        self.pages = {}


    def addSection(self, section, name, link=None, cl='', icon=False, order=0):
        self.pages[section] = {
            'name': name,
            'link': link,
            'icon': icon,
            'class': cl,
            'order': order,
            'menu': []
        }


    def add(self, section, name, link, cl='', icon=False, order=0):
        self.pages[section]['menu'].append({
            'name': name,
            'link': link,
            'class': cl,
            'order': order,
            'icon': icon
        })

    def get(self):
        return self.pages

    def getSection(self, section):
        return self.pages[section]


pebmynSideBar = MySideBar()


def register_sidebar(section, name, link, icon=False):
    def wrapper(fn):
        @functools.wraps
        def wrapper_inner(*args, **kwargs):
            pebmynSideBar.add(section=section, name=name, icon=icon, link=link)
            return fn(*args, **kwargs)
        #wrapper_inner.__name__ = fn.__name__
        return wrapper_inner

    return wrapper
