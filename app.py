import bcrypt
import connexion
from connexion import NoContent
from flask_cors import CORS
import db
import scraper
import jwt
import six
from werkzeug.exceptions import Unauthorized

db_config = {
    "host": "192.168.10.10",
    "database": "trippity",
    "user": "homestead",
    "password": "secret"
}

auth_config = {
    "jwt_secret": "trippitySecret2020"
}


def generate_token(email):
    return jwt.encode({"email": email}, auth_config["jwt_secret"], algorithm='HS256')


def decode_token(token):
    try:
        return jwt.decode(token, auth_config["jwt_secret"], algorithms=['HS256'])
    except Exception as e:
        six.raise_from(Unauthorized, e)


def create_user(body):
    connection, cur = db.get_db_connection(db_config)
    user_obj = {
        "name": body["name"],
        "email": body["email"],
        "password": bcrypt.hashpw(body["password"].encode('utf-8'), bcrypt.gensalt())
    }

    db.insert_user(connection, cur, user_obj)

    return {"bearer_token": generate_token(body["email"]).decode()}, 201


def login(body):
    connection, cur = db.get_db_connection(db_config)
    user = db.get_user_by_email(cur, body["email"])

    if user is None or len(user) == 0:
        return NoContent, 404

    if bcrypt.checkpw(body["password"].encode('utf-8'), user[0][3].encode('utf-8')):
        return {"bearer_token": generate_token(body["email"]).decode()}, 200

    return NoContent, 401


def get_countries():
    connection, cur = db.get_db_connection(db_config)
    countries = db.get_countries_list(cur)
    arr_countries = []
    for country in countries:
        arr_countries.append({
            "id": country[0],
            "name": country[1]
        })

    return arr_countries, 200


def get_trips():
    connection, cur = db.get_db_connection(db_config)
    trips = db.get_trips_list(cur)

    arr_trips = []
    for trip in trips:
        arr_trips.append({
            "description": trip[2],
            "id": trip[0],
            "image": trip[3],
            "name": trip[1]
        })

    return arr_trips, 200


def create_trip(body):
    connection, cur = db.get_db_connection(db_config)
    email = decode_token(connexion.request.headers['Authorization'].split(" ")[1])["email"]

    trip_obj = {
        "name": body["name"],
        "description": body["description"],
        "image": body["image"],
        "country_id": body["country_id"]
    }
    cities = body["cities"]
    id = db.insert_trip(connection, cur, trip_obj, email)

    for city in cities:
        city["trip_id"] = id
        db.insert_trip_cities(connection, cur, city)

    return NoContent, 201


def get_trip(id):
    connection, cur = db.get_db_connection(db_config)
    trip = db.get_trip(cur, id)
    cities = db.get_trip_cities_by_trip_id(cur, id)
    countries = db.get_countries_list(cur)
    country_obj = {}
    for country in countries:
        if (country[0] == trip[0][4]):   #If country ID == trip's country ID
            country_obj = {
                "id" : country[0],
                "name" : country[1]
            }
    cities_list = []
    for city in cities:
        temp, temp_desc = scraper.get_forecast(city[1])
        obj = {
            "id"                    : city[0],
            "name"                  : city[1],
            "datetime_of_arrival"   : city[2].strftime("%Y-%m-%d %H:%M:%S"),
            "datetime_of_departure" : city[3].strftime("%Y-%m-%d %H:%M:%S"),
            "temperature_in_kelvin": temp,
            "temp_desc": temp_desc
        }
        cities_list.append(obj)


    ret_obj = {
        "id"            :   trip[0][0],
        "name"          :   trip[0][1],
        "description"   :   trip[0][2],
        "image"         :   trip[0][3],
        "country"       :   country_obj,
        "cities"        :   cities_list
    }
    return ret_obj, 200


def update_trip(id, body):
    connection, cur = db.get_db_connection(db_config)
    trip_obj = {
        "name": body["name"],
        "description": body["description"],
        "image": body["image"],
        "country_id": body["country_id"]
    }
    db.update_trip(connection, cur, trip_obj, id)
    cities = body["cities"]

    city_list = db.get_trip_cities_by_trip_id(cur, id)
    for city in city_list:
        db.delete_trip_city(connection, cur, city[0])

    for city in cities:
        city["trip_id"] = id
        db.insert_trip_cities(connection, cur, city)

    return NoContent, 200


def delete_trip(id):
    connection, cur = db.get_db_connection(db_config)
    delete = db.delete_trip(connection, cur, id)
    return delete, 200


app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)
