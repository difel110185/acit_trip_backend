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
    connection = db.getDbConnection()
    cur = connection.cursor()
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
    connection = db.getDbConnection()
    cur = connection.cursor()
    name = trip["name"]
    image = trip["image"]
    description = trip["description"]
    country_id = trip["country_id"]
    db.insert_trip(connection, cur, name, description, image, country_id)
    return NoContent, 201

#/trip/{id} Functions
def get_trip(id):
    connection = db.getDbConnection()
    cur = connection.cursor()
    trip = db.get_trips_list(cur, id)
    return trip, 200 #Return Empty String with Status Code 200

def update_trip(id, trip):
    connection = db.getDbConnection()
    cur = connection.cursor()
    cities = trip["cities"]
    city = cities[0]
    arrival = city["date_of_arrival"]
    departure = city["date_of_departure"]
    print(arrival)
    print(departure)
    blah = db.update_trip(connection, cur, arrival, departure, id)
    return blah, 200

def delete_trip(id):
    connection = db.getDbConnection()
    cur = connection.cursor()
    tada = db.delete_trip(connection, cur, id)
    return tada, 200

app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)  # Filename = app & Variable = app ^^^^
app.app.config['CORS_HEADERS'] = 'Content-Type' #CORS -> Domain to Domain Stuff
app.add_api("openapi.yaml") #Adding openapi.yaml file

if __name__ == "__main__":
    app.run(port=8080)