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
    return currencyRates

if __name__ == "__main__":
    currencyRates = get_currencyRates()
    print(currencyRates)