import app
import mysql.connector
import unittest
import datetime
class TestAPI(unittest.TestCase):
    #Input: Nothing
    #Output: List of Dictionaries Containing Trip Information
    #Test: Does the Format equal what we want
    def test_getTrips(self):
        """
        Strips keys from input dict and mock dict, and asserts keys match
        TODO: Match value data types
        """
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
        trip_dict = trip_list[0]

        key_chain = []
        for key in trip_dict.keys:
            key_chain.append(key)

        data_chain = []
        for key in type_dict.keys():
            data_chain.append(key)

        self.assertEqual(key_chain, data_chain)

        value_type = []
        for value in trip_dict.values:
            value_type.append(type(value))

        data_type = []
        for value in type_dict.values():
            data_type.append(value)

        self.assertEqual(value_type, data_type)




    #Input: Trip Information
    #Output: Nothing
    #Test: Does the Input Provide the Necessary Information in the Correct Format
    def test_createTrip(self):
        status_code = app.create_trip()
        self.assertEqual(status_code, 201)


    #Input: ID of a Single Trip
    #Output: Trip Information for the Trip with the Given ID
    #Test: Is the Outputted Information that of Trip with the Given ID
    def test_getTrip(self):
        """TODO Check Response for type str"""
        response, status_code = app.get_trip()
        self.assertEqual(status_code, 200)

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

        trip_list = app.get_trip()
        trip_dict = trip_list[0]

        key_chain = []
        for key in trip_dict.keys:
            key_chain.append(key)

        data_chain = []
        for key in type_dict.keys():
            data_chain.append(key)

        self.assertEqual(key_chain, data_chain)

        value_type = []
        for value in trip_dict.values:
            value_type.append(type(value))

        data_type = []
        for value in type_dict.values():
            data_type.append(value)

        self.assertEqual(value_type, data_type)

    #Input: ID of a Trip & Information
    #Output: Nothing
    #Test: Is the Info in Mysql changed for the Trip with the Given ID
    def test_UpdateTrip(self):
        response, status_code = app.update_trip()
        self.assertEqual(status_code, 200)

    #Input: ID of a Trip
    #Output: Nothing
    #Test: Does the Mysql with Trip of given ID Exist?
    def test_DeleteTrip(self):
        response, status_code = app.delete_trip()
        self.assertEqual(status_code, 200)


if __name__ == '__main__':
    unittest.main()