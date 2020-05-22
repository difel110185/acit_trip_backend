import bcrypt
import connexion
from connexion import NoContent
from flask import current_app
from flask_cors import CORS
import db
import scraper
import jwt
import six
import amenitites
from werkzeug.exceptions import Unauthorized

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
    user_obj = {
        "name": body["name"],
        "email": body["email"],
        "password": bcrypt.hashpw(body["password"].encode('utf-8'), bcrypt.gensalt())
    }

    current_app.config["DATABASE"].insert_user(user_obj)

    return {"bearer_token": generate_token(body["email"]).decode()}, 201


def login(body):
    user = current_app.config["DATABASE"].get_user_by_email(body["email"])

    if user is None or len(user) == 0:
        return NoContent, 404

    if bcrypt.checkpw(body["password"].encode('utf-8'), user[0][3].encode('utf-8')):
        return {"bearer_token": generate_token(body["email"]).decode()}, 200

    return NoContent, 401


def get_countries():
    countries = current_app.config["DATABASE"].get_countries_list()

    arr_countries = []

    for country in countries:
        arr_countries.append({
            "id": country[0],
            "name": country[1]
        })

    return arr_countries, 200


def get_trips():
    email = decode_token(connexion.request.headers['Authorization'].split(" ")[1])["email"]

    trips = current_app.config["DATABASE"].get_trips_list(email)

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
    email = decode_token(connexion.request.headers['Authorization'].split(" ")[1])["email"]

    trip_obj = {
        "name": body["name"],
        "description": body["description"],
        "image": body["image"],
        "country_id": body["country_id"]
    }
    cities = body["cities"]
    id = current_app.config["DATABASE"].insert_trip(trip_obj, email)

    for city in cities:
        city["trip_id"] = id
        current_app.config["DATABASE"].insert_trip_cities(city)

    return NoContent, 201


def get_trip(id):
    email = decode_token(connexion.request.headers['Authorization'].split(" ")[1])["email"]

    trip = current_app.config["DATABASE"].get_trip(id, email)
    if trip is not None and len(trip) > 0:
        cities = current_app.config["DATABASE"].get_trip_cities_by_trip_id(id)
        countries = current_app.config["DATABASE"].get_countries_list()
        country_obj = {}
        for country in countries:
            if (country[0] == trip[0][4]):
                country_obj = {
                    "id" : country[0],
                    "name" : country[1]
                }
        cities_list = []
        for city in cities:
            yelp = amenitites.info(city[1])
            if yelp == None:
                yelp = {
                    "location": "Country not Supported",
                    "name": "Country not Supported",
                    "phone": "Country not Supported",
                    "price": "Country not Supported",
                    "rating": "Country not Supported",
                    "url": "",
                }
            temp, temp_desc = scraper.get_forecast(city[1])
            obj = {
                "id"                    : city[0],
                "name"                  : city[1],
                "datetime_of_arrival"   : city[2].strftime("%Y-%m-%d %H:%M:%S"),
                "datetime_of_departure" : city[3].strftime("%Y-%m-%d %H:%M:%S"),
                "temperature_in_kelvin": temp,
                "temp_desc": temp_desc,
                "location": yelp["location"],
                "yelpname": yelp["name"],
                "phone": yelp["phone"],
                "price": yelp["price"],
                "rating": yelp["rating"],
                "url": yelp["url"]
            }
            cities_list.append(obj)


        ret_obj = {
            "id"            :   trip[0][0],
            "name"          :   trip[0][1],
            "description"   :   trip[0][2],
            "image"         :   trip[0][3],
            "country"       :   country_obj,
            "cities"        :   cities_list,
            "currency"      :   scraper.api_get_currency("Canada", 1, country_obj["name"]),
            "currencies"    :   scraper.get_currencyRates()
        }

        return ret_obj, 200

    return NoContent, 404


def update_trip(id, body):
    email = decode_token(connexion.request.headers['Authorization'].split(" ")[1])["email"]

    trip = current_app.config["DATABASE"].get_trip(id, email)
    if trip is None or len(trip) == 0:
        return NoContent, 404

    trip_obj = {
        "name": body["name"],
        "description": body["description"],
        "image": body["image"],
        "country_id": body["country_id"]
    }
    current_app.config["DATABASE"].update_trip(trip_obj, id, email)
    cities = body["cities"]

    city_list = current_app.config["DATABASE"].get_trip_cities_by_trip_id(id)
    for city in city_list:
        current_app.config["DATABASE"].delete_trip_city(city[0])

    for city in cities:
        city["trip_id"] = id
        current_app.config["DATABASE"].insert_trip_cities(city)

    return NoContent, 200


def delete_trip(id):
    email = decode_token(connexion.request.headers['Authorization'].split(" ")[1])["email"]

    trip = current_app.config["DATABASE"].get_trip(id, email)
    if trip is None or len(trip) == 0:
        return NoContent, 404

    current_app.config["DATABASE"].delete_trip(id, email)

    return NoContent, 200


app = connexion.FlaskApp(__name__, specification_dir="")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")
app.app.config['DATABASE'] = db

if __name__ == "__main__":
    app.run(port=8080)
