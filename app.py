# -*- coding: utf-8 -*-

# import Flask from module "flask"
from flask import Flask


# create a new web application object
application = Flask(__name__)


# add a new route 
# http://localhost:5000/
@application.route('/')
def index():
    return "<h1>Hello World</h1>"


if __name__ == '__main__':
    application.run()
