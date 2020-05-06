import requests
import urllib
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def get_currencyRates():
    currencyRates = {}
    URL = 'http://www.bankofcanada.ca/rates/exchange/daily-exchange-rates/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find(id='table_daily_1')
    rows = table.find_all('tr', class_='bocss-table__tr')
    for row in rows:
        countries = row.find_all('th')
        tempCountry = ""
        for country in countries:
            tempCountry = country.text.strip()
        rates = row.find_all('td')
        tempRate = ""
        for rate in rates:
            tempRate = rate.text.strip()
        currencyRates[tempCountry] = tempRate
    currencyRates["Canadian dollar"] = 1
    return currencyRates

def api_get_currency(cInput):
    currencyIn = cInput[0]
    value = cInput[1]
    currencyOut = cInput[2]
    rates = get_currencyRates()
    if currencyIn in rates:
        if currencyOut in rates:
            rate = float(rates[currencyIn]) / float(rates[currencyOut])
            rate = round(rate, 2)
            exchange = value * rate
            outcome = "The exchange rate from " + str(currencyIn) + " to " \
                      + str(currencyOut) + " is " + str(rate) + "! " \
                      + str(value) + " " + str(currencyIn) + " is equal to " \
                      +  str(exchange) + " " + str(currencyOut) + "!"
            print(outcome)
            return rate, exchange
        else:
            error = str(currencyOut) + " is not accepted Currency!"
            return error
    else:
        error = str(currencyIn) + " is not accepted Currency!"
        return error

def get_forecast(city):
    # Enter your API key here
    api_key = "1a952ac12b24c9c0a95151029212c83e"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()

    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":

        # store the value of "main"
        # key in variable y
        y = x["main"]

        # store the value corresponding
        # to the "temp" key of y
        current_temperature = y["temp"]

        # store the value corresponding
        # to the "pressure" key of y
        current_pressure = y["pressure"]

        # store the value corresponding
        # to the "humidity" key of y
        current_humidiy = y["humidity"]

        # store the value of "weather"
        # key in variable z
        z = x["weather"]

        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]

        # print following values
        print(" Temperature (in kelvin unit) = " +
              str(current_temperature) +
              "\n atmospheric pressure (in hPa unit) = " +
              str(current_pressure) +
              "\n humidity (in percentage) = " +
              str(current_humidiy) +
              "\n description = " +
              str(weather_description))

    else:
        print(" City Not Found ")


if __name__ == "__main__":
    cInput = ["US dollar", 100, "Brazilian real"]
    output = api_get_currency(cInput)
    print(output)
    city = "Vancouver"
    get_forecast(city)