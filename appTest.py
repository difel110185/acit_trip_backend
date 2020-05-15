import mysql.connector
import unittest
import datetime
import connexion
import json
import db

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml")

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
                "datetime_of_arrival": "2020-05-05 21:42:37",
                "datetime_of_departure": "2020-05-05 21:42:37"
            }

        ]
    }
    validUser = {
        "name" : "validName",
        "email" : "valid@email.com",
        "password" : "Abc123"
    }
    dbConfig = {
        "host": "localhost",
        "database": "testdb",
        "user": "tripitty",
        "password": "123456"
    }
    def getAllTripIDs(self):
        connection, cursor = db.get_db_connection(self.dbConfig)
        query = """SELECT * FROM trips"""
        cursor.execute(query)
        trips = cursor.fetchall()
        ids = []
        for trip in trips:
            ids.append(trip[0])
        return ids

    #@classmethod
    def setUp(self):
        self.client = app.app.test_client()
        response = self.client.post('/users', data=json.dumps(self.validUser), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        loginResponse = self.client.post('/login', data=json.dumps(self.validUser), content_type="application/json")
        self.assertEqual(loginResponse.status_code, 200)
        loginToken = "Bearer {}".format(json.loads(loginResponse.data.decode())['bearer_token'])
        self.headers = {"Content-Type":"application/json", "Authorization": loginToken}

    #@classmethod
    def tearDown(self):
        pass

    def test_getCountries(self):
        """Test of app.get_countries() -> list, 200"""
        rv = self.client.get('/countries', headers=self.headers)
        self.assertEqual(rv.status_code, 200)

    def test_createTrip(self):
        """Test of app.create_trip(trip: dict) -> object, 201"""
        response = self.client.post('/trips', data=json.dumps(self.trip_obj), content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_getTrips(self):
        """Test of get_trips() -> [{}, {}, {}]"""
        response = self.client.get('/trips', headers=self.headers)
        trip_list = json.loads(response.data.decode())
        if len(trip_list) > 1:
            trip_dict = trip_list[0]

            value_type = []
            for value in trip_dict.values():
                value_type.append(type(value))

            data_type = []
            data_type.append(type(self.trip_obj['description']))
            data_type.append(type(self.trip_obj['id']))
            data_type.append(type(self.trip_obj['image']))
            data_type.append(type(self.trip_obj['name']))

            self.assertEqual(value_type, data_type)

    def test_getTrip(self):
        """Test of app.get_trip(id: int) -> trip: dict, 200"""
        idList = self.getAllTripIDs();
        if idList != []:
            id = idList[0]
            response = self.client.get('/trips/{}'.format(id), headers=self.headers, content_type="application/json")
            trip = json.loads(response.data.decode())
            self.assertIsInstance(trip, dict, 'Argument is of wrong type')
            value_type = []
            for value in trip.values():
                print(type(value))
                value_type.append(type(value))

            data_type = []
            data_type.append(type(self.trip_obj['cities']))
            data_type.append(type(self.trip_obj['cities'][0]))
            data_type.append(type(self.trip_obj['description']))
            data_type.append(type(self.trip_obj['id']))
            data_type.append(type(self.trip_obj['image']))
            data_type.append(type(self.trip_obj['name']))

            self.assertEqual(value_type, data_type)

    def test_updateTrip(self):
        """Test of app.update_trip(id: int, trip: dict) -> object, 200"""
        newObj = {
            "id": 1,
            "name": "second",
            "description": "desc2",
            "image": "img2",
            "country_id": 39,
            "cities": [
                {
                    "name": "Burnaby",
                    "datetime_of_arrival": "2021-05-05 21:42:37",
                    "datetime_of_departure": "2021-05-05 21:42:37"
                }

            ]
        }

        idList = self.getAllTripIDs();
        if idList != []:
            id = idList[0]
            response = self.client.put('/trips/{}'.format(id), data=json.dumps(newObj), headers=self.headers, content_type="application/json")
            self.assertEqual(response.status_code, 200)


    def test_deleteTrip(self):
        """Test of app.delete_trip(id: int) -> str, 200"""
        idList = self.getAllTripIDs()
        if idList != []:
            id = idList[0]
            response = self.client.delete('/trips/{}'.format(id), headers = self.headers, content_type = "application/json")
            self.assertTrue(response)
            self.assertEqual(response.status_code, 200, 'ERROR 404: File not found')


if __name__ == '__main__':
    unittest.main()
