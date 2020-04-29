# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='root',
    PASSWORD='password'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='trippity',
                                             user='root',
                                             password='password')
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to database {}".format(error))

def init_db():
    db = get_db()
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    g.db = connect_db();
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    """

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.cursor()
    cur.execute("""SELECT * FROM countries""")
    countries = cur.fetchall()
    cur.execute("""SELECT * FROM trip_cities""")
    cities = cur.fetchall()
    cur.execute("""SELECT * FROM trips""")
    trips = cur.fetchall()
    return render_template('show_entries.html', countries=countries, cities=cities, trips=trips)

@app.route('/add', methods=['POST'])
def add_entry():
    """
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
    """

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
    """

@app.route('/logout')
def logout():
    """
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
    """