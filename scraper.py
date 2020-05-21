import requests
import urllib
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

#Weather API from: https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/

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

def api_get_currency(currencyInput, value, currencyOutput):
    #Assign currencyIn to currency
    currencyIn = currencyInput.lower()
    currencyOut = currencyOutput.lower()
    if currencyIn == "canada":
        currencyIn = "Canadian dollar"
    elif currencyIn == "australia" or currencyIn == "christmas island" or currencyIn == "cocos (keeling) islands" or \
            currencyIn == "heard island and mcdonald islands" or currencyIn == "kiribati" or currencyIn == "nauru" or \
            currencyIn == "norfolk island" or currencyIn == "tuvalu":
        currencyIn = "Australian dollar"
    elif currencyIn == "brazil":
        currencyIn = "Brazilian real"
    elif currencyIn == "china":
        currencyIn = "Chinese renminbi"
    elif currencyIn == "austria" or currencyIn == "belgium" or currencyIn == "cyprus" or \
            currencyIn == "estonia" or currencyIn == "finland" or currencyIn == "france" or \
            currencyIn == "germany" or currencyIn == "greece" or currencyIn == "ireland" or \
            currencyIn == "italy" or currencyIn == "latvia" or currencyIn == "lithuania" or \
            currencyIn == "luxembourg" or currencyIn == "malta" or currencyIn == "netherlands" or \
            currencyIn == "netherlands antilles" or currencyIn == "portugal" or currencyIn == "slovakia" or \
            currencyIn == "slovenia" or currencyIn == "spain":
        currencyIn = "European euro"
    elif currencyIn == "hong kong":
        currencyIn = "Hong Kong dollar"
    elif currencyIn == "india" or currencyIn == "bhutan":
        currencyIn = "Indian rupee"
    elif currencyIn == "indonesia":
        currencyIn = "Indonesian rupiah"
    elif currencyIn == "japan":
        currencyIn = "Japanese yen"
    elif currencyIn == "mexico":
        currencyIn = "Mexican peso"
    elif currencyIn == "new zealand" or currencyIn == "niue" or currencyIn == "pitcairn" or \
            currencyIn == "tokelau" or currencyIn == "cook islands":
        currencyIn = "New Zealand dollar"
    elif currencyIn == "norway" or currencyIn == "svalbard and jan mayen" or currencyIn == "bouvet island":
        currencyIn = "Norwegian krone"
    elif currencyIn == "peru":
        currencyIn = "Peruvian new sol"
    elif currencyIn == "russian federation":
        currencyIn = "Russian ruble"
    elif currencyIn == "saudi arabia":
        currencyIn = "Saudi riyal"
    elif currencyIn == "singapore":
        currencyIn = "Singapore dollar"
    elif currencyIn == "south africa" or currencyIn == "lesotho" or currencyIn == "namibia":
        currencyIn = "south african rand"
    elif currencyIn == "south korea":
        currencyIn = "South Korean won"
    elif currencyIn == "sweden":
        currencyIn = "swedish krona"
    elif currencyIn == "switzerland" or currencyIn == "liechtenstein":
        currencyIn = "Swiss franc"
    elif currencyIn == "taiwan, province of china":
        currencyIn = "Taiwanese dollar"
    elif currencyIn == "turkey":
        currencyIn = "Turkish lira"
    elif currencyIn == "british indian ocean territory" or currencyIn == "united kingdom":
        currencyIn = "UK pound sterling"
    elif currencyIn == "virgin islands, u.s." or currencyIn == "united states" or currencyIn == "united states minor outlying islands" or \
            currencyIn == "guam" or currencyIn == "puerto rico" or currencyIn == "american samoa" or currencyIn == "virgin islands, british" or \
            currencyIn == "northern mariana islands" or currencyIn == "united states minor outlying islands" or currencyIn == "togo" or \
            currencyIn == "timor-leste" or currencyIn == "panama" or currencyIn == "palau" or currencyIn == "federated states of micronesia" or \
            currencyIn == "marshall islands" or currencyIn == "haiti" or currencyIn == "el salvador" or currencyIn == "ecuador" or \
            currencyIn == "british indian ocean territory":
        currencyIn = "US dollar"
    #Assign currencyOut to currency
    if currencyOut == "canada":
        currencyOut = "Canadian dollar"
    elif currencyOut == "australia" or currencyOut == "christmas island" or currencyOut == "cocos (keeling) islands" or \
         currencyOut == "heard island and mcdonald islands" or currencyOut == "kiribati" or currencyOut == "nauru" or \
         currencyOut == "norfolk island" or currencyOut == "tuvalu":
        currencyOut = "Australian dollar"
    elif currencyOut == "brazil":
        currencyOut = "Brazilian real"
    elif currencyOut == "china":
        currencyOut = "Chinese renminbi"
    elif currencyOut == "austria" or currencyOut == "belgium" or currencyOut == "cyprus" or \
            currencyOut == "estonia" or currencyOut == "finland" or currencyOut == "france" or \
            currencyOut == "germany" or currencyOut == "greece" or currencyOut == "ireland" or \
            currencyOut == "italy" or currencyOut == "latvia" or currencyOut == "lithuania" or \
            currencyOut == "luxembourg" or currencyOut == "malta" or currencyOut == "netherlands" or \
            currencyOut == "netherlands antilles" or currencyOut == "portugal" or currencyOut == "slovakia" or \
            currencyOut == "slovenia" or currencyOut == "spain":
        currencyOut = "European euro"
    elif currencyOut == "hong kong":
        currencyOut = "Hong Kong dollar"
    elif currencyOut == "india" or currencyOut == "bhutan":
        currencyOut = "Indian rupee"
    elif currencyOut == "indonesia":
        currencyOut = "Indonesian rupiah"
    elif currencyOut == "japan":
        currencyOut = "Japanese yen"
    elif currencyOut == "mexico":
        currencyOut = "Mexican peso"
    elif currencyOut == "new zealand" or currencyOut == "niue" or currencyOut == "pitcairn" or \
         currencyOut == "tokelau" or currencyOut == "cook islands":
        currencyOut = "New Zealand dollar"
    elif currencyOut == "norway" or currencyOut == "svalbard and jan mayen" or currencyOut == "bouvet island":
        currencyOut = "Norwegian krone"
    elif currencyOut == "peru":
        currencyOut = "Peruvian new sol"
    elif currencyOut == "russian federation":
        currencyOut = "Russian ruble"
    elif currencyOut == "saudi arabia":
        currencyOut = "Saudi riyal"
    elif currencyOut == "singapore":
        currencyOut = "Singapore dollar"
    elif currencyOut == "south africa" or currencyIn == "lesotho" or currencyIn == "namibia":
        currencyOut = "south african rand"
    elif currencyOut == "south korea":
        currencyOut = "South Korean won"
    elif currencyOut == "sweden":
        currencyOut = "swedish krona"
    elif currencyOut == "switzerland" or currencyOut == "liechtenstein":
        currencyOut = "Swiss franc"
    elif currencyOut == "taiwan, province of china":
        currencyOut = "Taiwanese dollar"
    elif currencyOut == "turkey":
        currencyOut = "Turkish lira"
    elif currencyOut == "british indian ocean territory" or currencyOut == "united kingdom":
        currencyOut = "UK pound sterling"
    elif currencyOut == "virgin islands, u.s." or currencyOut == "united states" or currencyOut == "united states minor outlying islands" or \
            currencyOut == "guam" or currencyOut == "puerto rico" or currencyOut == "american samoa" or currencyOut == "virgin islands, british" or \
            currencyOut == "northern mariana islands" or currencyOut == "united states minor outlying islands" or currencyOut == "togo" or \
            currencyOut == "timor-leste" or currencyOut == "panama" or currencyOut == "palau" or currencyOut == "federated states of micronesia" or \
            currencyOut == "marshall islands" or currencyOut == "haiti" or currencyOut == "el salvador" or currencyOut == "ecuador" or \
            currencyOut == "british indian ocean territory":
        currencyOut = "US dollar"

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
            #print(outcome)
            return rate
        else:
            return 0
    else:
        return 0


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
        #print(" Temperature (in kelvin unit) = " +
        #      str(current_temperature) +
        #      "\n atmospheric pressure (in hPa unit) = " +
        #      str(current_pressure) +
        #      "\n humidity (in percentage) = " +
        #      str(current_humidiy) +
        #      "\n description = " +
        #      str(weather_description))
        return current_temperature, weather_description
    else:
        print(" City Not Found ")

def get_acceptedCurrencies():
    rates = get_currencyRates()
    accepted = []
    for each in rates:
        accepted.append(each)
    return accepted
if __name__ == "__main__":
    output = api_get_currency("Canada", 1, "Brazil")
    print(output)

    currencies = get_acceptedCurrencies()
    print(currencies)

    city = "Vancouver"
    temp = get_forecast(city)
    print(temp)
