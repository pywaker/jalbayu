# -*- coding: utf-8 -*-

# import Flask from module "flask"
from flask import Flask, render_template


# create a new web application object
application = Flask(__name__)


# add a new route 
# http://localhost:5000/
@application.route('/')
def index():
    return render_template('hello.html')


if __name__ == '__main__':
    application.run(debug=True)
