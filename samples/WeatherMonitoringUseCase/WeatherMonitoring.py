import requests
import os
from OntologyToAPI.core.Connectors.Stateless.APIConnection import APIConnection

async def WeatherMonitoring(args):
    API_KEY = os.getenv("WEATHER_API_KEY")
    if args["FromMetadata"]:
        Latitude = args["FromMetadata"]["LEMLatitude_R"][0]["LEMLatitude"]
        Longitude = args["FromMetadata"]["LEMLongitude_R"][0]["LEMLongitude"]
    else:
        Latitude = args["FromParameters"]["Latitude"]
        Longitude = args["FromParameters"]["Longitude"]
    api = APIConnection({"hasRequestURL": "http://api.weatherapi.com/v1/current.json"})
    return api.exec_query(f"?key={API_KEY}&q={Latitude},{Longitude}")