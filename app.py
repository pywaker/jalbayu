# -*- coding: utf-8 -*-

# import Flask from module "flask"
from flask import Flask, render_template, request


# create a new web application object
application = Flask(__name__)


# add a new route 
# http://localhost:5000/
@application.route('/')
def index():
    return render_template('home.html')


@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # save this data to db or do something
        print("Posted data", request.form)
    return render_template('login.html')


if __name__ == '__main__':
    
    application.run(debug=True)
