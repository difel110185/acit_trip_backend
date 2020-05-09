import app
import mysql.connector
import unittest
import datetime


class TestAPI(unittest.TestCase):
    """
    Test of functions in app.py
    """
    def test_getTrips(self):
        """Test of get_trips() -> [{}, {}, {}]"""
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
        for i in range(len(trip_list)):
            trip_dict = trip_list[i]

            key_chain = []
            for key in trip_dict.keys():
                key_chain.append(key)

            data_chain = []
            for key in type_dict.keys():
                data_chain.append(key)

            value_type = []
            for value in trip_dict.values():
                value_type.append(type(value))

            data_type = []
            for value in type_dict.values():
                data_type.append(type(value))

            self.assertEqual(key_chain, data_chain)
            self.assertEqual(value_type, data_type)

    def test_createTrip(self):
        """Test of app.create_trip(trip: str) -> NoContent, 201"""
        no_content, status_code = app.create_trip()
        self.assertEqual(status_code, 201)

    def test_getTrip(self):
        """Test of app.get_trip(id: int) -> trip: dict, 200"""
        response, status_code = app.get_trip()
        self.assertIsInstance(response, dict, 'Argument is of wrong type')
        self.assertEqual(status_code, 200, 'ERROR 404: File not found')

    def test_UpdateTrip(self):
        """Test of app.update_trip(id: int, trip: str) -> str, 200"""
        response, status_code = app.update_trip()
        self.assertIsInstance(response, str, 'Argument is of wrong type')
        self.assertEqual(status_code, 200, 'ERROR 404: File not found')

    def test_DeleteTrip(self):
        """Test of app.delete_trip(id: int) -> str, 200"""
        response, status_code = app.delete_trip()
        self.assertIsInstance(response, str, 'Argument is of wrong type')
        self.assertEqual(status_code, 200, 'ERROR 404: File not found')


if __name__ == '__main__':
    unittest.main()