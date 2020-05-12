import mysql.connector
from mysql.connector import Error


def insert_trip(database_connection, cursor, trip, email):
    query = """INSERT INTO trips (name, description, image, country_id, user_id) VALUES (%s, %s, %s, %s, (SELECT id FROM users WHERE email = %s))"""

    try:
        cursor.execute(query, (trip['name'], trip['description'], trip['image'], trip['country_id'], email))
        database_connection.commit()
        return cursor.lastrowid
    except Error as e:
        print("Error occured: ", e)
        print("Trip not inserted")


def insert_user(database_connection, cursor, user):
    query = """INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"""

    try:
        cursor.execute(query, (user['name'], user['email'], user['password'],))
        database_connection.commit()
        return cursor.lastrowid
    except Error as e:
        print("Error occurred: ", e)
        print("User not inserted")


def insert_trip_cities(database_connection, cursor, trip_city):
    query = """INSERT INTO trip_cities (name, datetime_of_arrival, datetime_of_departure, trip_id) VALUES (%s, %s, %s, '%s')"""

    try:
        cursor.execute(query, (trip_city['name'], trip_city['datetime_of_arrival'], trip_city['datetime_of_departure'], trip_city['trip_id'],))
        database_connection.commit()
    except Error as e:
        print("Error occurred: ", e)
        print("City not inserted")


def delete_trip(database_connection, cursor, id: int, email):
    query = """DELETE FROM trips WHERE id = %s and user_id = (SELECT id FROM users WHERE email = %s)"""

    try:
        cursor.execute(query, (id, email, ))
        database_connection.commit()
        print("Trip ID: ", id, " deleted from trips table")
    except Error as e:
        print("Error occurred: ", e)
        print("Trip ID: ", id, " not deleted")


def delete_trip_city(database_connection, cursor, id: int):
    query = """DELETE FROM trip_cities WHERE id = '%s'"""

    try:
        cursor.execute(query, (id,))
        database_connection.commit()
        print(id, " deleted from trip cities table")
    except Error as e:
        print("Error occurred: ", e)
        print(id, " not deleted")


def get_countries_list(cursor):
    query = """SELECT * FROM countries"""

    try:
        cursor.execute(query)
        countries_list = cursor.fetchall()
        return countries_list
    except Error as e:
        print("Error occurred: ", e)


def get_trips_list(cursor, email):
    query = """SELECT * FROM trips WHERE user_id = (SELECT id FROM users WHERE email = %s)"""

    try:
        cursor.execute(query, (email, ))
        trips_list = cursor.fetchall()
        return trips_list
    except Error as e:
        print("Error occurred: ", e)


def get_trip(cursor, id: int, email):
    query = """SELECT * FROM trips WHERE id = %s and user_id = (SELECT id FROM users WHERE email = %s)"""

    try:
        cursor.execute(query, (id, email, ))
        trip = cursor.fetchall()
        return trip
    except Error as e:
        print("Error occurred: ", e)


def get_user_by_email(cursor, email):
    query = """SELECT * FROM users WHERE email = %s"""

    try:
        cursor.execute(query, (email,))
        user = cursor.fetchall()
        return user
    except Error as e:
        print("Error occurred: ", e)


def get_trip_cities_by_trip_id(cursor, trip_id):
    query = """SELECT * FROM trip_cities WHERE trip_id = '%s'"""

    try:
        cursor.execute(query, (trip_id,))
        trips_cities = cursor.fetchall()
        return trips_cities
    except Error as e:
        print("Error occurred: ", e)


def update_trip_cities(database_connection, cursor, trip_city, id: int):
    query = """UPDATE trip_cities SET name = %s, datetime_of_arrival = %s, datetime_of_departure = %s WHERE id= '%s'"""

    try:
        cursor.execute(query, (trip_city['name'], trip_city['datetime_of_arrival'], trip_city['datetime_of_departure'], id,))
        database_connection.commit()
    except Error as e:
        print("Error occurred: ", e)
        print("Trip cities ID: ", id, " not updated")


def update_trip(database_connection, cursor, trip, id, email):
    query = """UPDATE trips SET name = %s, description = %s, image = %s, country_id = '%s' WHERE id = %s and user_id = (SELECT id FROM users WHERE email = %s)"""

    try:
        cursor.execute(query, (trip['name'], trip['description'], trip['image'], trip['country_id'], id, email, ))
        database_connection.commit()
    except Error as e:
        print("Error occurred: ", e)
        print("Trip ID: ", id, " not updated")


def get_db_connection(db_config):
    try:
        connection = mysql.connector.connect(host=db_config["host"],
                                            database=db_config["database"],
                                            user=db_config["user"],
                                            password=db_config["password"])
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as error:
        print("Failed to connect to database {}".format(error))


def close_db_connection(connection):
    try:
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to close database connection {}".format(error))
