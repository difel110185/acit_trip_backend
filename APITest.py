import app
import mysql.connector
import unittest
import datetime
class TestAPI(unittest.TestCase):
    #Input: Nothing
    #Output: List of Dictionaries Containing Trip Information
    #Test: Does the Format equal what we want
    def test_getAllTrips(self):
        type_dict = {
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
        trip_list = app.get_trips()
        self.assertDictEqual(trip_list, type_dict)

    #Input: Trip Information
    #Output: Nothing
    #Test: Does the Input Provide the Necessary Information in the Correct Format
    def test_createTrip(self):
        response = app.create_trip()
        self.assertTrue(response.status_code == 201)


    #Input: ID of a Single Trip
    #Output: Trip Information for the Trip with the Given ID
    #Test: Is the Outputted Information that of Trip with the Given ID
    def test_GettingTrip(self):
        """Response body"""
        response = app.get_trip()
        self.assertTrue(response.status_code == 200)

    #Input: ID of a Trip & Information
    #Output: Nothing
    #Test: Is the Info in Mysql changed for the Trip with the Given ID
    def test_UpdateTrip(self):
        response = app.update_trip()
        self.assertTrue(response.status_code == 200)

    #Input: ID of a Trip
    #Output: Nothing
    #Test: Does the Mysql with Trip of given ID Exist?
    def test_DeleteTrip(self):
        response = app.delete_trip()
        self.assertTrue(response.status_code == 200)


if __name__ == '__main__':
    unittest.main()