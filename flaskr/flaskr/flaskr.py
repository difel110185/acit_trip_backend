# all the imports
import os
import mysql.connector

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from mysql.connector import Error
from mysql.connector import errorcode
from flask_swagger import swagger
from flask_restplus import Resource, Api
from werkzeug.debug import console

app = Flask(__name__) # create the application instance :)
api = Api(app, version='1.0')
ns = api.namespace('simple', description='Im so confused')

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
    """Opens a new database connection"""
    g.db = connect_db()
    return g.db

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

@ns.route('/trips')
class Trips(Resource):
    def get(self):
        db = get_db()
        cur = db.cursor()
        cur.execute("""SELECT * FROM trips""")
        trips = cur.fetchall()
        console.log(trips)
        return trips


@app.route('/trips/{id}')
def all_trips():
    tomato = ""
    return tomato