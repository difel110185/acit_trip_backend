import connexion
from connexion import NoContent
from flask_cors import CORS
import db


db_config = {
    "host": "192.168.10.10",
    "database": "trippity",
    "user": "homestead",
    "password": "secret"
}


def get_countries():
    connection, cur = db.getDbConnection(db_config)
    countries = db.get_countries_list(cur)
    arrCountries = [];
    for each in countries:
        tempdict = {
            "id": each[0],
            "name": each[1]
        }
        arrCountries.append(tempdict)

    return arrCountries, 200


def get_trips():
    connection, cur = db.getDbConnection(db_config)
    trips = db.get_trips_list(cur)
    arrTrips = [];
    for each in trips:
        tempdict = {
            "description": each[2],
            "id": each[0],
            "image": each[3],
            "name": each[1]
        }
        arrTrips.append(tempdict)

    return arrTrips, 200


def create_trip(trip):
    connection, cur = db.getDbConnection(db_config)
    tripObj = {
        "name": trip["name"],
        "description": trip["description"],
        "image":trip["image"],
        "country_id":trip["country_id"]
    }
    cities = trip["cities"]
    id = db.insert_trip(connection, cur, tripObj)

    for city in cities:
        city["trip_id"] = id
        db.insert_trip_cities(connection, cur, city)

    return NoContent, 201

#/trip/{id} Functions
def get_trip(id):
    connection, cur = db.getDbConnection(db_config)
    trip = db.get_trip(cur, id)
    cities = db.get_trip_cities_by_trip_id(cur, id)
    countries = db.get_countries_list(cur)
    countryObj = {}
    for country in countries:
        if (country[0] == trip[0][4]):   #If country ID == trip's country ID
            countryObj = {
                "id" : country[0],
                "name" : country[1]
            }

    cities_list = []
    for city in cities:
        obj = {
            "id"                    : city[0],
            "name"                  : city[1],
            "datetime_of_arrival"   : city[2].strftime("%Y-%m-%d %H:%M:%S"),
            "datetime_of_departure" : city[3].strftime("%Y-%m-%d %H:%M:%S")
        }
        cities_list.append(obj)

    retObj = {
        "id"            :   trip[0][0],
        "name"          :   trip[0][1],
        "description"   :   trip[0][2],
        "image"         :   trip[0][3],
        "country"       :   countryObj,
        "cities"        :   cities_list
    }
    return retObj, 200 #Return Empty String with Status Code 200

def update_trip(id, trip):
    connection, cur = db.getDbConnection(db_config)
    #break apart trip object into trip and cities
    tripObj = {
        "name": trip["name"],
        "description": trip["description"],
        "image": trip["image"],
        "country_id": trip["country_id"]
    }
    db.update_trip(connection, cur, tripObj, id)
    cities = trip["cities"]

    #remove existing cities and replace with new ones
    cityList = db.get_trip_cities_by_trip_id(cur, id)
    for city in cityList:
        db.delete_trip_city(connection, cur, city[0])
    #removed from here

    for city in cities:
        city["trip_id"] = id
        db.insert_trip_cities(connection, cur, city)

    return NoContent, 200

def delete_trip(id):
    connection, cur = db.getDbConnection(db_config)
    delete = db.delete_trip(connection, cur, id)
    return delete, 200

app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)  # Filename = app & Variable = app ^^^^
app.app.config['CORS_HEADERS'] = 'Content-Type' #CORS -> Domain to Domain Stuff
app.add_api("openapi.yaml") #Adding openapi.yaml file

if __name__ == "__main__":
    app.run(port=8080)
