import uvicorn
from Generator.APIGenerator import Generator

if __name__ == "__main__":
    APIGen = Generator(showLogs=True)
    APIGen.load_ontologies(paths=[
        "Samples/PB_UseCase/RealizationOntologies/SmartLEM-PB_LEM.ttl"
    ])
    APIGen.load_ontologies(paths=[
        "Samples/PB_UseCase/RealizationOntologies/SmartLEM-EqualProsumerBiddingBusinessModel.ttl"
    ])
    APIGen.load_ontologies(paths=[
        "Samples/WeatherMonitoring_UseCase/RealizationOntologies/SmartLEM-Weather_LEM.ttl"
    ])
    # APIGen.load_ontologies(paths=[
    #     "Samples/WeatherMonitoring_UseCase/RealizationOntologies/SmartLEM-WeatherBusinessModel.ttl"
    # ])
    APIGen.serialize_ontologies()
    api_app = APIGen.generate_api_routes()
    uvicorn.run(api_app, host="127.0.0.1", port=5000)