import uvicorn
from Generator.APIGenerator import Generator

if __name__ == "__main__":
    APIGen = Generator(showLogs=True)
    APIGen.load_ontologies(paths=[
        "Samples/PB_UseCase/RealizationOntologies/SmartLEM-PB_LEM.ttl",
        "Samples/PB_UseCase/RealizationOntologies/SmartLEM-EqualProsumerBiddingBusinessModel.ttl"
    ])
    api_app = APIGen.generate_api_routes()
    uvicorn.run(api_app, host="127.0.0.1", port=5000)