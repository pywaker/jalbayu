# -*- coding: utf-8 -*-

import os
# import sqlite3
# used to change the filename to secure format
# from werkzeug.utils import secure_filename
# import Flask from module "flask"
from flask import Flask, render_template, request, g, redirect
from flask_login import (LoginManager, login_user, login_required, logout_user,
                         current_user)


# basepath is current directory path of this application
BASEPATH = os.path.dirname(os.path.abspath(__file__))

print(BASEPATH)

# create a new web application object
application = Flask(__name__)

# application configurations
# application.config['UPLOAD_FOLDER'] = os.path.join(BASEPATH, 'static/uploads')
application.config['SECRET_KEY'] = 'kaskdjh9213nkwej923fnkwvjnc92kejrvnkv93vkejv93'


# initialize login manager provided by flask_login
login_manager = LoginManager()
login_manager.init_app(application)

# DATABASE = 'data/db.sqlite3'


class User:
    
    users = ({
        'username': 'test@example.net',
        'password': 'pass1'          
    },
    {
        'username': 'test2@example.net',
        'password': 'pass2'          
    }
    )
    authenticated = False

    # this will reflect our current loggedin user
    user = {}
    
    def is_authenticated(self):
        """
        return True if user is successfully authenticated/loggedin
        """
        return self.authenticated
    
    def is_active(self):
        """
        check if loggedin user is currently disabled or not
        """
        return True
    
    def is_anonymous(self):
        """
        is user anonymous ? / applicable for guest users
        """
        return False
    
    def get_id(self):
        """
        return unique ID of the user, this will be stored in session 
        cookie to identify user later
        """
        if self.is_authenticated():
            return self.user['username']
        return None
    
    @staticmethod
    def user_exists(email, password):
        # check username and password exists in users tuple
        user_dct = [dct for dct in User.users if dct['username'] == email 
                    and dct['password'] == password]
        print("found user", user_dct)
        if user_dct:
            user = User()
            user.user = user_dct[0]
            user.authenticated = True
            return user
        return None


@login_manager.user_loader
def load_user(user_id):
    user_dct = [dct for dct in User.users if dct['username'] == user_id]
    user = User()
    user.user = user_dct[0]
    user.authenticated = True
    return user


# def get_db():
#    # g._database if g._database exists else None
#    # getattribute
#    db = getattr(g, '_database', None)
#    if db is None:
#        db = g._database = sqlite3.connect(DATABASE)
#    return db


# @application.teardown_appcontext
# def close_connection(exception):
#    db = getattr(g, '_database', None)
#    if db is not None:
#        db.close()


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


@application.route('/login', methods=['GET', 'POST'])
def login():
    """
    here we validate username and password provided by user
    and login them.
    """
    print("Current user", current_user)
    if request.method == 'POST':
        # save this data to db or do something
        print("Posted data", request.form)
        # check if requested user is in our database
        user = User.user_exists(request.form['email'], request.form['password'])
        if user:
            login_user(user)
            print("logged in")
        else:
            print("Unable to login")
    return render_template('login.html')


@application.route('/logout')
def logout():
    """
    here we logout user
    """
    logout_user()
    return redirect('/')


#@application.route('/data/add', methods=['GET', 'POST'])
#@login_required
#def add_data():
#    if request.method == 'POST':
#        # upload data file to server
#        # save entry into db
#       db = get_db()
#        cur = db.cursor()
#        # print what we need to save to db
#        print(request.form['name'], request.files['datafile'].filename)
#        
#        file = request.files['datafile']
#        filename = None
#        if file:
#            filename = secure_filename(file.filename)
#            print(filename)
#            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
#        
#        # save submitted details to db
#        sql = 'INSERT INTO dataset(name, dataset) VALUES(?, ?)'
#        cur.execute(sql, (request.form['name'], filename))
#        db.commit()
        
#    return render_template('data_add.html')


if __name__ == '__main__':
    application.run(debug=True)

