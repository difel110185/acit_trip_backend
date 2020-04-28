import os
import mysql.connector
import json
from mysql.connector import Error
from mysql.connector import errorcode
from flask import Flask

# def insert_db(cursor, name: Str, description: Str, image_path: Str, country_id: Int):
#     pass

#PRE: database connection
#POST: returns array of countries and their ID
#PARAM: cursor for SQL database
def get_countries_list(cursor):
    query = """SELECT * FROM countries"""
    cursor.execute(query)
    countries = cursor.fetchall()
    print(type(countries))
    for row in countries:
        print("ID: =", row[0])
        print("Country name: =", row[1])
    return countries

#PRE: database connection
#POST: returns array of all trips OR array of all trips OF USER
#PARAM: cursor for SQL database, username if specified
def get_trips_list(cursor, user="_default_"):
    if (user != "_default_"):
        query = """SELECT * FROM trips WHERE name = %s"""
        cursor.execute(query, (user,))
        trips_list = cursor.fetchall()
        return trips_list
    else:
        query = """SELECT * FROM trips"""
        cursor.execute(query)
        trips_list = cursor.fetchall()
        return trips_list

#PRE: database connection, trip
#POST:
#PARAM:
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

if __name__ == "__main__":
    connection = getDbConnection()
    cursor = connection.cursor()
    get_countries_list(cursor)






    closeDbConnection(connection)
