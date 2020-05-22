import mysql.connector
from mysql.connector import Error


def insert_trip(trip, email):
    return 1


def insert_user(user):
    return 1


def insert_trip_cities(trip_city):
    pass


def delete_trip(id: int, email):
    pass


def delete_trip_city(id: int):
    pass


def get_countries_list():
    return [[1, "Canada"], [2, "Brazil"]]


def get_trips_list(email):
    return [[0, "string", "string", "string", 1], [0, "string", "string", "string", 2]]


def get_trip(id: int, email):
    if id == 1:
        return [[0, "string", "string", "string", 1, 1]]

    return list()


def get_user_by_email(email):
    if email != "fail@gmail.com":
        return [[1, "John Traveller", "john@gmail.com", "$2b$12$DOV.s0B4ECVtNtb1Qtm8Q.woeMrWaxYs/OpzGbemsCDgDmcjR/Mly"]]

    return list()


def get_trip_cities_by_trip_id(trip_id):
    return list()


def update_trip_cities(trip_city, id: int):
    pass


def update_trip(trip, id, email):
    pass

