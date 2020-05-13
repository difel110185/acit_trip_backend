import app
import mysql.connector
import unittest
import datetime


class TestAPI(unittest.TestCase):
    """
    Test of functions in app.py
    """
    trip_obj = {
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

    def test_getCountries(self):
        """Test of app.get_countries() -> list, 200"""
        response, status_code = app.get_countries()
        self.assertIsInstance(response, list, 'Argument is of wrong type')
        self.assertEqual(status_code, 200, 'ERROR 404: File not found')

    def test_getTrips(self):
        """Test of get_trips() -> [{}, {}, {}]"""
        trip_list = app.get_trips()
        for i in range(len(trip_list)):
            trip_dict = trip_list[i]

            value_type = []
            for value in trip_dict.values():
                value_type.append(type(value))

            data_type = []
            for value in self.trip_obj.values():
                data_type.append(type(value))

            self.assertEqual(value_type, data_type)

    def test_createTrip(self):
        """Test of app.create_trip(trip: dict) -> object, 201"""
        no_content, status_code = app.create_trip(self.trip_obj)
        self.assertTrue(no_content)
        self.assertEqual(status_code, 201)

    def test_getTrip(self):
        """Test of app.get_trip(id: int) -> trip: dict, 200"""
        mock_id = self.trip_obj["id"]
        response, status_code = app.get_trip(mock_id)
        self.assertIsInstance(response, dict, 'Argument is of wrong type')
        self.assertEqual(status_code, 200, 'ERROR 404: File not found')

        value_type = []
        for value in response.values():
            value_type.append(type(value))

        data_type = []
        for value in self.trip_obj.values():
            data_type.append(type(value))

        self.assertEqual(value_type, data_type)

    def test_updateTrip(self):
        """Test of app.update_trip(id: int, trip: dict) -> object, 200"""
        mock_id = self.trip_obj["id"]
        no_content, status_code = app.update_trip(mock_id, self.trip_obj)
        self.assertTrue(no_content)
        self.assertEqual(status_code, 200, 'ERROR 404: File not found')

    def test_deleteTrip(self):
        """Test of app.delete_trip(id: int) -> str, 200"""
        mock_id = self.trip_obj["id"]
        response, status_code = app.delete_trip(mock_id)
        self.assertTrue(response)
        self.assertEqual(status_code, 200, 'ERROR 404: File not found')


if __name__ == '__main__':
    unittest.main()
