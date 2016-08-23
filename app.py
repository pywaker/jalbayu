# -*- coding: utf-8 -*-

# import Flask from module "flask"
from flask import Flask, render_template


# create a new web application object
application = Flask(__name__)


# add a new route 
# http://localhost:5000/
@application.route('/hello/<name>')
def index(name):
    """
    this function which is initiated when this route
    is called, is view function.
    """
    # again we are passing name to template
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    application.run(debug=True)
