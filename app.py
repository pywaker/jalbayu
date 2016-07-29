# -*- coding: utf-8 -*-

import os
# import sqlite3
# used to change the filename to secure format
from werkzeug.utils import secure_filename
# import Flask from module "flask"
from flask import Flask, render_template, request, g, redirect
from flask_login import (LoginManager, login_user, login_required, logout_user,
                         current_user)
from flask_sqlalchemy import SQLAlchemy


# basepath is current directory path of this application
BASEPATH = os.path.dirname(os.path.abspath(__file__))

print(BASEPATH)

# create a new web application object
application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = os.path.join(BASEPATH, 'static/uploads')
application.config['SECRET_KEY'] = 'kaskdjh9213nkwej923fnkwvjnc92kejrvnkv93vkejv93'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEPATH, 
                                                                            'data/db.sqlite3')

db = SQLAlchemy(application)

# initialize login manager provided by flask_login
login_manager = LoginManager()
login_manager.init_app(application)

# DATABASE = 'data/db.sqlite3'


#def get_db():
#    # g._database if g._database exists else None
#    # getattribute
#    db = getattr(g, '_database', None)
#    if db is None:
#        db = g._database = sqlite3.connect(DATABASE)
#    return db
#
#
#@application.teardown_appcontext
#def close_connection(exception):
#    db = getattr(g, '_database', None)
#    if db is not None:
#        db.close()


class User(db.Model):
    """
    Model == Model from MVC ( Model View Controller )
    """
    # db attributes
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(60))
    status = db.Column(db.Boolean, default=True)


class User:
    
#    users = ({
#        'username': 'test@example.net',
#        'password': 'pass1'          
#    },)
#    authenticated = False
#    user = {}
    
    def is_authenticated(self):
	"""
        return True if user is successfully authenticated/loggedin
        """
#        return self.authenticated
        return self.id and True
    
    def is_active(self):
	"""
        check if loggedin user is currently disabled or not
        """
#        return True
        return self.status
    
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
        return self.id
#        if self.is_authenticated():
##            return self.user['username']
#            return self.user['id']
#        return None
    
#    @staticmethod
#    def user_exists(email, password):
##        user_dct = [dct for dct in User.users if dct['username'] == email 
##                    and dct['password'] == password]
#        cur = get_db().cursor()
#        user_sql = "SELECT id, username FROM users WHERE username=? AND password=?"
#        cur.execute(user_sql, (email, password))
#        user_record = cur.fetchone()
#        print("record found", user_record)
##        print("found user", user_dct)
##        if user_dct:
#        if user_record:
#            user = User()
##            user.user = user_dct[0]
#            user.user = {
#                'id': user_record[0],
#                'username': user_record[1]
#            }
#            user.authenticated = True
#            return user
#        return None


class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    dataset = db.Column(db.String(250))
    
    def __repr__(self):
        return self.name


@login_manager.user_loader
def load_user(user_id):
#    cur = get_db().cursor()
#    user_sql = "SELECT id, username FROM users WHERE id=?"
#    cur.execute(user_sql, (user_id,))
#    user_record = cur.fetchone()
##    user_dct = [dct for dct in User.users if dct['username'] == user_id]
#    user = User()
##    user.user = user_dct[0]
#    user.user = {
#        'id': user_record[0],
#        'username': user_record[1]
#    }
#    user.authenticated = True
    user = User.query.get(user_id)
    return user


@application.route('/initdb')
def initdb():
    """
    this view will initialize database and insert dummy users to it
    """
    db = get_db()
    cur = db.cursor()

    create_sql = """CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                       username TEXT NOT NULL, 
                                       password TEXT NOT NULL, 
                                       status INTEGER)"""

    cur.execute(create_sql)

    insert_sql = """INSERT INTO users(username, password, status)
                    VALUES('test1@example.net', 'pass1', 1),
                          ('test2@example.net', 'pass2', 1)"""
    cur.execute(insert_sql)
    db.commit()
    return 'OK'


# add a new route 
# http://localhost:5000/
@application.route('/hello/<name>')
def index(name):
    """
    this view which is initiated when this route
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
#        user = User.user_exists(request.form['email'], request.form['password'])
        user = User.query.filter_by(username=request.form['email'],
                                    password=request.form['password']).first()
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


@application.route('/data/add', methods=['GET', 'POST'])
@login_required
def add_data():
    if request.method == 'POST':
        # upload data file to server
        # save entry into db
#        db = get_db()
#        cur = db.cursor()
        # print what we need to save to db
        print(request.form['name'], request.files['datafile'].filename)
        
        file = request.files['datafile']
        filename = None
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        
        # save submitted details to db
#        sql = 'INSERT INTO dataset(name, dataset) VALUES(?, ?)'
#        cur.execute(sql, (request.form['name'], filename))
#        db.commit()
        dataset = Dataset(name=request.form['name'],
                          dataset=filename)
        db.session.add(dataset)
        db.session.commit()
        
    return render_template('data_add.html')


if __name__ == '__main__':
    
    application.run(debug=True)
