import connexion
import os
import mysql.connector
import json
import datetime
from mysql.connector import Error, cursor
from mysql.connector import errorcode
from connexion import NoContent
from flask_cors import CORS
import db



#/trip Functions
def get_trips():
    connection, cur = db.getDbConnection()
    trips = db.get_trips_list(cur)
    arrTrips = [];
    for each in trips:
        tempdict = {
            "description": each[2],
            "id": each[0],
            "image": each[3],
            "name": each[1]
        }
        arrTrips.append(tempdict)

    return arrTrips, 200 #Return Empty String with Status Code 200


def create_trip(trip):
    connection, cur = db.getDbConnection()
    db.insert_trip(connection, cur, trip)
    return NoContent, 201

#/trip/{id} Functions
def get_trip(id):
    connection, cur = db.getDbConnection()
    trip = db.get_trip(cur, id)
    return trip, 200 #Return Empty String with Status Code 200

def update_trip(id, trip):
    connection, cur = db.getDbConnection()
    blah = db.update_trip(connection, cur, trip, id)
    return blah, 200

def delete_trip(id):
    connection, cur = db.getDbConnection()
    tada = db.delete_trip(connection, cur, id)
    return tada, 200

app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)  # Filename = app & Variable = app ^^^^
app.app.config['CORS_HEADERS'] = 'Content-Type' #CORS -> Domain to Domain Stuff
app.add_api("openapi.yaml") #Adding openapi.yaml file

if __name__ == "__main__":
    app.run(port=8080)