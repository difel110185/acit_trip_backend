import unittest

import connexion
import json
import dbTest

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml")
app.app.config['DATABASE'] = dbTest

class TestAPI(unittest.TestCase):
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

    def setUp(self):
        self.client = app.app.test_client()
        response = self.client.post('/users', data=json.dumps(self.validUser), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        login_token = "Bearer {}".format(json.loads(response.data.decode())['bearer_token'])
        self.headers = {"Content-Type":"application/json", "Authorization": login_token}

    def tearDown(self):
        pass

    def test_getCountries(self):
        rv = self.client.get('/countries', headers=self.headers)
        self.assertEqual(rv.status_code, 200)

    def test_login(self):
        response = self.client.post('/login', data=json.dumps({
            "email" : "valid@email.com",
            "password" : "Abc123"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_login_not_found(self):
        response = self.client.post('/login', data=json.dumps({
            "email" : "fail@gmail.com",
            "password" : "Abc123"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_login_unauthorized(self):
        response = self.client.post('/login', data=json.dumps({
            "email" : "valid@email.com",
            "password" : "XUXA"
        }), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_create_trip(self):
        response = self.client.post('/trips', data=json.dumps(self.trip_obj), content_type="application/json", headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_get_trips(self):
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

    def test_get_trip(self):
        response = self.client.get('/trips/1'.format(id), headers=self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_trip_not_found(self):
        response = self.client.get('/trips/2'.format(id), headers=self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_update_trip(self):
        response = self.client.put('/trips/1', data=json.dumps({
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
        }), headers=self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_update_trip_not_found(self):
        response = self.client.put('/trips/2', data=json.dumps({
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
        }), headers=self.headers, content_type="application/json")
        self.assertEqual(response.status_code, 404)

    def test_deleteTrip(self):
        response = self.client.delete('/trips/1', headers = self.headers, content_type = "application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_trip_not_found(self):
        response = self.client.delete('/trips/2', headers = self.headers, content_type = "application/json")
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
