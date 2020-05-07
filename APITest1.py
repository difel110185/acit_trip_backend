import app
import mysql.connector
import unittest
import datetime


class TestAPI(unittest.TestCase):
    #Input: Nothing
    #Output: List of Dictionaries Containing Trip Information
    #Test: Does the Format equal what we want
    def test_getAllTrips(self):
        connection, cursor = db.getDbConnection()
        trip_mock = [
            {
                "description": "first trip",
                "id": "0",
                "image": "A",
                "name": "A"
            }
        ]
        db.insert_trip(connection, cursor, trip_mock)
        result = get_trips()
        format = (result[0][1], result[0][2], result[0][3], result[0][4])
        if isinstance(result, list) is true:
            self.assertEqual(format, ("first trip", "0", "A", "A"))


    #Input: Trip Information
    """
    {
        "id": 0,
        "name": "string",
        "description": "string",
        "image": "string",
        "country_id": 0,
        "cities": [
            {
                "name": "string",
                "date_of_arrival": "2020-05-05T21:42:37.061Z",
                "date_of_departure": "2020-05-05T21:42:37.061Z"
            }
        ]
    }
    """
    #Output: Nothing
    #Test: Does the Input Provide the Necessary Information in the Correct Format
    def test_createTrip(self):
        connection, cursor = db.getDbConnection()
        trip_mock = {
            "id": 0,
            "name": "string",
            "description": "string",
            "image": "string",
            "country_id": 0,
            "cities": [
                {
                    "name": "string",
                    "date_of_arrival": "2020-05-05T21:42:37.061Z",
                    "date_of_departure": "2020-05-05T21:42:37.061Z"
                }
            ]
        }
        db.creat_trip(connection, cursor, trip_mock)
        result = cursor.fetchall()
        self.assertEqual(trip_mock, result)


    #Input: ID of a Single Trip
    #Output: Trip Information for the Trip with the Given ID
    #Test: Is the Outputted Information that of Trip with the Given ID
    def test_GettingTrip(self):
        trip = get_trip(id)
        trip_id = trip['id']
        self.assertEqual(id, trip_id)


    #Input: ID of a Trip & Information
    #Output: Nothing
    #Test: Is the Info in Mysql changed for the Trip with the Given ID
    def test_UpdateTrip(self):
        connection, cursor = db.getDbConnection()
        origin_trip = {
            "id": 0,
            "name": "First",
            "description": "The first trip",
            "image": "string",
            "country_id": 0,
            "cities": [
                {
                    "name": "string",
                    "date_of_arrival": "2020-05-05T21:42:37.061Z",
                    "date_of_departure": "2020-05-05T21:42:37.061Z"
                }
            ]
        }
        db.insert_trip(connection, cursor, origin_trip)
        update_trip = {
            "id": 1,
            "name": "string",
            "description": "string",
            "image": "string",
            "country_id": 0,
            "cities": [
                {
                    "name": "string",
                    "date_of_arrival": "2020-05-05T21:42:37.061Z",
                    "date_of_departure": "2020-05-05T21:42:37.061Z"
                }
            ]
        }
        db.update_trip(connection, cursor, 0, update_trip)
        result = cursor.fetchall()
        self.assertEqual(update_trip, result)


    #Input: ID of a Trip
    #Output: Nothing
    #Test: Does the Mysql with Trip of given ID Exist?
    def test_DeleteTrip(self):
        connection, cursor = db.getDbConnection()
        trip_mock = [
            {
                "description": "first trip",
                "id": "0",
                "image": "A",
                "name": "A"
            }
        ]
        db.insert_trip(connection, cursor, trip_mock)
        db.delete_trip(connection, cursor, 0)
        trips_list = cursor.fetchall()
        self.assertNotIn(trip_mock, trips_list)

