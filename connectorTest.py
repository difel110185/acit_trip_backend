import db
import unittest


class TestTrippity(unittest.TestCase):
    db_config = {
        "host": "localhost",
        "database": "testdb",
        "user": "root",
        "password": ""
    }

    #WORKS
    def test_Connection(self):
        connection, cursor = db.getDbConnection(self.db_config)
        self.assertTrue(connection)
        self.assertTrue(cursor)

    # WORKS
    def test_tripInsertDelete(self):
        connection, cursor = db.getDbConnection(self.db_config)
        trip_mock = {
            'name': 'First trip',
            'description': 'This is the first trip.',
            'image': 'Image parsed as string',
            'country_id': 38 #Canada
        }
        db.insert_trip(connection, cursor, trip_mock)
        #check if inserted properly
        query = """SELECT * FROM trips"""
        cursor.execute(query)
        result = cursor.fetchall()
        grabbed = (result[0][1], result[0][2], result[0][3], result[0][4])
        self.assertEqual(grabbed, ('First trip', 'This is the first trip.', 'Image parsed as string', 38))
        id = result[0][0]
        db.delete_trip(connection, cursor, id)

    # WORKS
    def test_trip_citiesInsertDelete(self):
        connection, cursor = db.getDbConnection(self.db_config)

        trip_mock = {
            'name': 'First trip',
            'description': 'This is the first trip.',
            'image': 'Image parsed as string',
            'country_id': 38 #Canada
        }
        db.insert_trip(connection, cursor, trip_mock)
        query1 = """SELECT * FROM trips"""
        cursor.execute(query1)
        result = cursor.fetchall()
        tripId = result[0][0]


        arrive = '2020-01-01 10:00:00'
        departure = '2020-01-05 10:00:00'
        city_mock = {
            'name': 'First city',
            'datetime_of_arrival' : arrive,
            'datetime_of_departure' : departure,
            'trip_id' : tripId
        }
        db.insert_trip_cities(connection, cursor, city_mock)
        query2 = """SELECT * FROM trip_cities"""
        cursor.execute(query2)
        result = cursor.fetchall()
        cityId = result[0][0]
        grabbed = (result[0][1], result[0][2].strftime("%Y-%m-%d %H:%M:%S"), result[0][3].strftime("%Y-%m-%d %H:%M:%S"), result[0][4])
        self.assertEqual(grabbed, ('First city', arrive, departure, tripId))
        db.delete_trip_city(connection, cursor, cityId)
        db.delete_trip(connection, cursor, tripId)

    # WORKS
    def test_getTripsList(self):
        connection, cursor = db.getDbConnection(self.db_config)
        trip1_mock = {
            'name': 'First trip',
            'description': 'This is the first trip.',
            'image': 'Image parsed as string',
            'country_id': 38 #Canada
        }
        trip2_mock = {
            'name': 'Second trip',
            'description': 'This is the second trip.',
            'image': 'Image parsed as string',
            'country_id': 39 #Cape Verde
        }
        db.insert_trip(connection, cursor, trip1_mock)
        db.insert_trip(connection, cursor, trip2_mock)
        query = """SELECT * FROM trips"""
        cursor.execute(query)
        trips_list = cursor.fetchall()
        test_list = db.get_trips_list(cursor)
        trip1Id = test_list[0][0]
        trip2Id = test_list[1][0]
        self.assertEqual(trips_list, test_list)
        db.delete_trip(connection, cursor, trip1Id)
        db.delete_trip(connection, cursor, trip2Id)

    # WORKS
    def test_updateTrip(self):
        connection, cursor = db.getDbConnection(self.db_config)
        trip_original = {
            'name' : 'Original',
            'description' : 'Unchanged',
            'image' : 'first',
            'country_id' : 38 # Canada
        }
        db.insert_trip(connection, cursor, trip_original)
        query = """SELECT * FROM trips"""
        cursor.execute(query)
        result = cursor.fetchall()
        original_id = result[0][0]


        trip_modified = {
            'name' : 'Modified',
            'description' : 'Changed',
            'image' : 'second',
            'country_id' : 39 #Cape Verde
        }
        db.update_trip(connection, cursor, trip_modified, original_id)
        cursor.execute(query)
        result = cursor.fetchall()
        grabbed = (result[0][1], result[0][2], result[0][3], result[0][4])
        self.assertEqual(grabbed, ('Modified', 'Changed', 'second', 39))
        db.delete_trip(connection, cursor, original_id)

    # WORKS
    def test_updateTripCity(self):
        connection, cursor = db.getDbConnection(self.db_config)
        trip_mock = {
            'name': 'First trip',
            'description': 'This is the first trip.',
            'image': 'Image parsed as string',
            'country_id': 38 #Canada
        }
        db.insert_trip(connection, cursor, trip_mock)
        query = """SELECT * FROM trips"""
        cursor.execute(query)
        result = cursor.fetchall()
        tripID = result[0][0]

        city_mock = {
            'name' : 'Vancouver',
            'datetime_of_arrival' : '2020-01-01 10:00:00',
            'datetime_of_departure' : '2020-01-02 10:00:00',
            'trip_id' : tripID
        }
        db.insert_trip_cities(connection, cursor, city_mock)
        query2 = """SELECT * FROM trip_cities"""
        cursor.execute(query2)
        result = cursor.fetchall()
        cityID = result[0][0]

        new_city_mock = {
            'name' : 'Toronto',
            'datetime_of_arrival' : '2020-05-01 10:00:00',
            'datetime_of_departure' : '2020-06-02 10:00:00'
        }
        db.update_trip_cities(connection, cursor, new_city_mock, cityID)
        cursor.execute(query2)
        result = cursor.fetchall()
        grabbed = (result[0][1], result[0][2].strftime("%Y-%m-%d %H:%M:%S"), result[0][3].strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(grabbed, ('Toronto', '2020-05-01 10:00:00', '2020-06-02 10:00:00'))
        db.delete_trip_city(connection, cursor, cityID)
        db.delete_trip(connection, cursor, tripID)

    def test_getTrip(self):
        connection, cursor = db.getDbConnection(self.db_config)
        trip_mock = {
            'name': 'First trip',
            'description': 'This is the first trip.',
            'image': 'Image parsed as string',
            'country_id': 38 #Canada
        }
        db.insert_trip(connection, cursor, trip_mock)
        query = """SELECT * FROM trips"""
        cursor.execute(query)
        result = cursor.fetchall()
        tripID = result[0][0]

        #Checking here
        trip = db.get_trip(cursor, tripID)
        compare = (tripID, trip_mock['name'], trip_mock['description'], trip_mock['image'], trip_mock['country_id'])
        self.assertEqual(trip[0], compare)
        db.delete_trip(connection, cursor, tripID)

if __name__ == "__main__":
    unittest.main()
