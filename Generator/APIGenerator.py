from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import List
import pprint, logging

from Generator.Utility import *
from Generator.Ontology import Ontology

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)

def create_metadata_handler(db_connector, query, name):
    async def handler():
        try:
            result = await db_connector.exec_query(query)
            return {"data": result}
        except Exception as e:
            logging.exception(f"Error running query for {name}")
            return {"error": str(e)}
    return handler

def create_business_model_handler(db_connectors: dict, required_metadata: list, external_function):
    async def handler():
        aggregated_res = {"conn": db_connectors}
        for md in required_metadata:
            pkg, name = md.name.split(":")
            try:
                aggregated_res[name] = await db_connectors[pkg].exec_query(md.hasSource.query)
            except Exception as e:
                logging.exception(f"Error running query for {name}")
                return {"error": str(e)}
        result = await external_function(aggregated_res)
        return {"data": result}
    return handler

class Generator:
    def __init__(self, ontologies: List[str]):
        self.ontology = Ontology(paths=ontologies)
        self.routes = []
        self.app = FastAPI()

        @self.app.get("/", include_in_schema=False)
        async def root():
            return RedirectResponse(url="/docs")

    def generate_routes(self) -> FastAPI:
        logging.info(f'Generating API routes for the available metadata...')
        for pkg_name, pkg_data in self.ontology.data.items():
            db_connector = pkg_data["CommTechnology"]
            for md in pkg_data["Metadata"]:
                if not md.hasSource or not md.hasSource.query:
                    continue  # Skip metadata without source query
                route_path = f"/{pkg_name}/{md.name.split(':')[-1]}"
                query = md.hasSource.query
                handler = create_metadata_handler(db_connector, query, md.name)
                self.app.add_api_route(
                    path=route_path,
                    endpoint=handler,
                    methods=["GET"],
                    name=md.hasSource.desc,
                    tags=[f"Metadata ({pkg_name})"],
                )
                logging.info(f'Added {md.name} API route...')
        logging.info(f'Generating API routes for the business models...')
        for bm_name, bm_dt in self.ontology.bms.items():
            name = bm_name.split(":")
            ec_func = import_function_from_file(filepath=bm_dt.externalCode.pythonFile, function_name=bm_dt.externalCode.function)
            handler = create_business_model_handler(bm_dt.communications, bm_dt.requiresMetadata, ec_func)
            self.app.add_api_route(
                path=f"/{name[0]}/{name[1]}/run",
                endpoint=handler,
                methods=["POST"],
                name=f"This endpoint executes the {bm_dt.name} business model, and retrieve it`s results.",
                tags=[f"Business Model ({bm_dt.name})"],
            )
            logging.info(f'Added {bm_name} running API route...')
        return self.app