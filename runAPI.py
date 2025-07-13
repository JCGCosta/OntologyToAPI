import uvicorn
from Generator.APIGenerator import Generator

if __name__ == "__main__":
    APIGen = Generator([
        "Samples/PB_UseCase/RealizationOntologies/SmartLEM-PB_LEM.ttl",
        "Samples/PB_UseCase/RealizationOntologies/SmartLEM-EqualProsumerBiddingBusinessModel.ttl"]
    )
    app = APIGen.generate_routes()
    uvicorn.run(app, host="127.0.0.1", port=5000)