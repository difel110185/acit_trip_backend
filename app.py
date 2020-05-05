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
    connection, cur = db.getDbConnection('testdb')
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
    connection, cur = db.getDbConnection('testdb')
    db.insert_trip(connection, cur, trip)
    return NoContent, 201

#/trip/{id} Functions
def get_trip(id):
    connection, cur = db.getDbConnection('testdb')
    trip = db.get_trip(cur, id)
    cities = db.get_trip_cities_by_trip_id(cur, id)
    countries = db.get_countries_list(cur)
    countryObj = {}
    for country in countries:
        if (country[0] == trip[0][4]):   #If country ID == trip's country ID
            countryObj = {
                "id" : country[0],
                "name" : country[1]
            }

    cities_list = []
    for city in cities:
        obj = {
            "id"                    : city[0],
            "name"                  : city[1],
            "datetime_of_arrival"   : city[2].strftime("%Y-%m-%d %H:%M:%S"),
            "datetime_of_departure" : city[3].strftime("%Y-%m-%d %H:%M:%S")
        }
        cities_list.append(obj)

    retObj = {
        "id"            :   trip[0][0],
        "name"          :   trip[0][1],
        "description"   :   trip[0][2],
        "image"         :   trip[0][3],
        "country"       : countryObj,
        "cities"        : cities_list
    }
    return retObj, 200 #Return Empty String with Status Code 200

def update_trip(id, trip):
    connection, cur = db.getDbConnection('testdb')
    update = db.update_trip(connection, cur, trip, id)
    return update, 200

def delete_trip(id):
    connection, cur = db.getDbConnection('testdb')
    delete = db.delete_trip(connection, cur, id)
    return delete, 200

app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)  # Filename = app & Variable = app ^^^^
app.app.config['CORS_HEADERS'] = 'Content-Type' #CORS -> Domain to Domain Stuff
app.add_api("openapi.yaml") #Adding openapi.yaml file

if __name__ == "__main__":
    app.run(port=8080)
