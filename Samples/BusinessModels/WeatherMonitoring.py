import requests
from Generator.Connectors.Stateless.APIConnection import APIConnection

async def WeatherMonitoring(args):
    API_KEY = "f73ff7f7b0504575998152153251407"
    Latitude = args["LEMLatitude_R"][0]["LEMLatitude"]
    Longitude = args["LEMLongitude_R"][0]["LEMLongitude"]
    api = APIConnection({"hasRequestURL": "http://api.weatherapi.com/v1/current.json"})
    return api.exec_query(f"?key={API_KEY}&q={Latitude},{Longitude}")