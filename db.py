import os
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

#PRE: database connection established, trips table must exist in database
#POST: inserts trip into database
#PARAM: database connection, cursor for SQL database, trip dictionary
def insert_trip(database_connection, cursor, trip):
    query = """INSERT INTO trips (name, description, image, country_id) VALUES (%s, %s, %s, %s)"""
    input = (trip['name'], trip['description'], trip['image'], trip['country_id'],)
    try:
        cursor.execute(query,input)
        database_connection.commit()
    except Error as e:
        print("Error occured: ", e)
        print("Trip not inserted")


#PRE: database connection established, trip cities table must exist in database
#POST: inserts trip cities into database
#PARAM: database connection, cursor for SQL database, trip city dictionary
def insert_trip_cities(database_connection, cursor, trip_city):
    query = """INSERT INTO trip_cities (name, datetime_of_arrival, datetime_of_departure, trip_id) VALUES (%s, %s, %s, %s)"""
    input = (trip_city['name'], trip_city['datetime_of_arrival'], trip_city['datetime_of_departure'], trip_city['trip_id'])
    try:
        cursor.execute(query, input)
        database_connection.commit()
    except Error as e:
        print("Error occured: ", e)
        print("Trip not inserted")

#PRE: database connection established, trip must exist inside database
#POST: deletes trip from database
#PARAM: database connection, cursor for SQL database, name of trip
def delete_trip(database_connection, cursor, id: int):
    query = """DELETE FROM trips WHERE id = %s"""
    try:
        cursor.execute(query, (id,))
        database_connection.commit()
        print(trip_name + " deleted from trips table")
    except Error as e:
        print("Error occured: ", e)
        print(trip_name + " not deleted")

#PRE: database connection established, at least one trip city must exist in database with corresponding trip_id
#POST: deletes trip city from database
#PARAM: database connection, cursor for SQL database, ID of trip_city
def delete_trip_city(database_connection, cursor, id: int):
    query = """DELETE FROM trip_cities WHERE id = %s"""
    try:
        cursor.execute(query, (id,))
        database_connection.commit()
        print(id + " deleted from trip cities table")
    except Error as e:
        print("Error occured: ", e)
        print(id + " not deleted")


# PRE: database connection
# POST: returns list of countries and their ID
# PARAM: cursor for SQL database
def get_countries_list(cursor):
    query = """SELECT * FROM countries"""
    cursor.execute(query)
    countries = cursor.fetchall()
    return countries

#PRE: database connection
#POST: returns list of all trips and their IDs
#PARAM: cursor for SQL database, ID if specified
def get_trips_list(cursor):
    query = """SELECT * FROM trips"""
    try:
        cursor.execute(query)
        trips_list = cursor.fetchall()
        return trips_list
    except Error as e:
        print("Error occured: ", e)

#PRE: database connection
#POST: returns trip of specified ID
#PARAM: cursor for SQL database, ID if specified
def get_trip(cursor, id: int):
    query = """SELECT * FROM trips WHERE id = %s"""
    try:
        cursor.execute(query, (id,))
        trip = cursor.fetchall()
        return trip
    except Error as e:
        print("Error occured: ", e)


#PRE: database connection, trip cities table exists
#POST: returns list of trip cities of selected trip_id
#PARAM: cursor for SQL database, ID of trip
def get_trip_cities_by_trip_id(cursor, trip_id):
    query = """SELECT * FROM trip_cities WHERE trip_id = %s"""
    cursor.execute(query, (trip_id,))
    trips_cities = cursor.fetchall()
    return trips_cities


#PRE: database connection, trip cities table exists
#POST: updates trip_cities defined by ID
#PARAM: database connection, cursor for SQL database, trip_city detail in dictionary, ID of trip_cities
def update_trip_cities(database_connection, cursor, trip_city, id: int):
    query = """UPDATE trip_cities SET name = %s, datetime_of_arrival = %s, datetime_of_departure = %s WHERE id= %s"""
    try:
        input = (trip_city['name'], trip_city['datetime_of_arrival'], trip_city['datetime_of_departure'], id,)
        cursor.execute(query, input)
        database_connection.commit()
    except Error as e:
        print("Error occured: ", e)
        print("Trip cities ID: " + id + " not updated")

#PRE: database connection, existing trip
#POST: updates trip defined by ID
#PARAM: database connection, cursor for SQL database, trip details in dictionary, ID of trip
def update_trip(database_connection, cursor, trip, id):
    query = """UPDATE trip SET name = %s, description = %s, image = %s, country_id = %s"""
    try:
        input = (trip['name'], trip['description'], trip['image'], trip['country_id'],)
        cursor.execute(query, input)
        database_connection.commit()
    except Error as e:
        print("Error occured: ", e)
        print("Trip ID: " + id + " not updated")

#PRE: SQL server is running with database 'trippity' existing
#POST: returns the connection to the SQL server
def getDbConnection():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='trippity',
                                            user='root',
                                            password='')
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as error:
        print("Failed to connect to database {}".format(error))


# PRE: SQL server must be connected
# POST: SQL connection closed
# PARAM: SQL server connection to be closed
def closeDbConnection(connection):
    try:
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to close database connection {}".format(error))
