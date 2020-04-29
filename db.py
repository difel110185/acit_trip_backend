import os
import mysql.connector
import json
import datetime
from mysql.connector import Error
from mysql.connector import errorcode

#PRE: database connection established, countries table must exist in database
#POST: inserts a country's name inside the database
#PARAM: database connection, cursor for SQL database, name of country
def insert_country(database_connection, cursor, country_name: str):
    query = """INSERT INTO countries (name) VALUES (%s)"""
    cursor.execute(query, (country_name,))
    database_connection.commit()

#PRE: database connection established, trips table must exist in database
#POST: inserts trip into database
#PARAM: database connection, cursor for SQL database, name of trip, description of trip, image location, country's ID
def insert_trip(database_connection, cursor, name: str, description: str, image: str, country_id: int):
    query = """INSERT INTO trips (name, description, image, country_id) VALUES (%s, %s, %s, %s)"""
    cursor.execute(query, (name, description, image, country_id))
    database_connection.commit()

#PRE: database connection established, trip cities table must exist in database
#POST: inserts trip cities into database
#PARAM: database connection, cursor for SQL database, name of city, arrival time, departure time, associated trip ID
def insert_trip_cities(database_connection, cursor, name: str, arrival: str, departure: str, trip_id: int):
    query = """INSERT INTO trip_cities (name, datetime_of_arrival, datetime_of_departure, trip_id)"""
    cursor.execute(query, (name, arrival, departure, trip_id))
    database_connection.commit()

#PRE: database connection
#POST: returns list of countries and their ID
#PARAM: cursor for SQL database
def get_countries_list(cursor):
    query = """SELECT * FROM countries"""
    cursor.execute(query)
    countries = cursor.fetchall()
    return countries

#PRE: database connection
#POST: returns list of all trips OR array of all trips OF USER
#PARAM: cursor for SQL database, username if specified
def get_trips_list(cursor, name="_default_"):
    #choose name of trip
    if (name != "_default_"):
        query = """SELECT * FROM trips WHERE name = %s"""
        cursor.execute(query, (name,))
        trips_list = cursor.fetchall()
        return trips_list
    else:
        query = """SELECT * FROM trips"""
        cursor.execute(query)
        trips_list = cursor.fetchall()
        return trips_list

#PRE: database connection, trip cities table exists
#POST: returns list of trip cities of selected trip_id
#PARAM: cursor for SQL database, ID of trip
def get_trip_cities(cursor, trip_id):
    query = """SELECT * FROM trip_cities WHERE trip_id = %s"""
    cursor.execute(query, (trip_id,))
    trips_cities = cursor.fetchall()
    return trip_cities


def getDbConnection():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='trippity',
                                            user='root',
                                            password='')
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to database {}".format(error))

def closeDbConnection(connection):
    try:
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to close database connection {}".format(error))
