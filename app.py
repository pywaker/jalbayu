# -*- coding: utf-8 -*-

import os
# import sqlite3
# used to change the filename to secure format
from werkzeug.utils import secure_filename
# import Flask from module "flask"
from flask import Flask, render_template, request, g, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy


BASEPATH = os.path.dirname(os.path.abspath(__file__))

print(BASEPATH)

# create a new web application object
application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = os.path.join(BASEPATH, 'static/uploads')
application.config['SECRET_KEY'] = 'kaskdjh9213nkwej923fnkwvjnc92kejrvnkv93vkejv93'
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEPATH, 
                                                                            'data/db.sqlite3')

db = SQLAlchemy(application)

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

#    users = ({
#        'username': 'test@example.net',
#        'password': 'pass1'          
#    },)
#    authenticated = False
#    user = {}
    
    def is_authenticated(self):
#        return self.authenticated
        return self.id and True
    
    def is_active(self):
#        return True
        return self.status
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
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


# add a new route 
# http://localhost:5000/
@application.route('/')
def index():
#    cur = get_db().cursor()
#    cur.execute('SELECT id, name, dataset from dataset')
#    records = cur.fetchall()
    records = Dataset.query.all()
    print(records)
    return render_template('home.html', records=records)


@application.route('/login', methods=['GET', 'POST'])
def login():
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
