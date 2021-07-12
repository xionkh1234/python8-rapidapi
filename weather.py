import requests
import json
import sys
import datetime

from os.path import getmtime, exists


class Weather:
    def __init__(self):
        self.resp = []
        self.forecast_data = {}
        self.counter = 0

    def get_response(self, key):
        url = "https://visual-crossing-weather.p.rapidapi.com/forecast"

        querystring = {"location":"Warszawa,Poland","aggregateHours":"24","shortColumnNames":"0","unitGroup":"metric","contentType":"json"}

        headers = {
            'x-rapidapi-key': key,
            'x-rapidapi-host': "visual-crossing-weather.p.rapidapi.com"
            }

        self.resp = requests.request("GET", url, headers=headers, params=querystring).json()

    def load_response(self, key, file):
        if not exists(file):
            self.get_resp(key)
            self.save_resp(file)
            return

        sec = getmtime(file)
        current = datetime.datetime.now().timestamp()
        if current - sec < 60 * 60 * 24:
            with open(file, "r") as f:
                self.resp = json.load(f)
        else:
            self.get_resp(key)
            self.save_resp(file)

    def save_response(self, file):
        with open(file, "w") as fp:
            file_content = json.dumps(self.resp)
            fp.write(file_content)
        return True

    def forecast(self):
        for current_value in self.resp["locations"]["Warszawa,Poland"]["values"]:
            date = datetime.datetime.utcfromtimestamp(current_value["datetime"] / 1000).strftime("%Y-%m-%d")
            daily_forecast = current_value["conditions"]
            self.forecast_data[date] = daily_forecast

    def __getitem__(self, item):
        if item not in self.forecast_data:
            return "I do not know."
        if "Rain" in self.forecast_data[item]:
            return "It does rain."
        else:
            return "It doesn't rain."

    def __iter__(self):
        self.counter = 0
        return self

    def items(self):
        return self.forecast_data.items()

    def __next__(self):
        if len(self.forecast_data) <= self.counter:
            raise StopIteration
        lista = list(self.forecast_data)[self.counter]
        self.counter += 1
        return lista


weather = Weather()
key = input()
outfile = sys.argv[1]
weather.load_resp(key, outfile)
weather.forecast()

if len(sys.argv) >= 3:
    print(weather[sys.argv[2]])
if len(sys.argv) < 3:
    x = datetime.date.today() + datetime.timedelta(days=1)
    y = x.strftime("%Y-%m-%d")
    print(weather[y])

for lista in weather:
    print(lista)
