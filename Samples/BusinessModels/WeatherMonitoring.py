import requests
import os
from Generator.Connectors.Stateless.APIConnection import APIConnection

async def WeatherMonitoring(args):
    API_KEY = os.getenv("WEATHER_API_KEY")
    Latitude = args["LEMLatitude_R"][0]["LEMLatitude"]
    Longitude = args["LEMLongitude_R"][0]["LEMLongitude"]
    api = APIConnection({"hasRequestURL": "http://api.weatherapi.com/v1/current.json"})
    return api.exec_query(f"?key={API_KEY}&q={Latitude},{Longitude}")