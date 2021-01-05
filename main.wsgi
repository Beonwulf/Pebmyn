#!/usr/bin/python/3.8
import sys

path = '/home/$USER/www/pebmyn'
if path not in sys.path:
    sys.path.append(path)

from main import app as application
