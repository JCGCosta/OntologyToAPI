import uvicorn
import sqlite3
from pathlib import Path
from OntologyToAPI.core.APIGenerator import APIGenerator

def configuring_a_sample_sqlite_database():
    if not Path('example.db').exists():
        with sqlite3.connect('example.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature_c FLOAT NOT NULL,
                    r_humidity FLOAT NOT NULL
                );
            ''')
            cursor.execute("INSERT INTO weather (temperature_c, r_humidity) VALUES ('21.5', '60');")
            cursor.execute("INSERT INTO weather (temperature_c, r_humidity) VALUES ('22.0', '58');")
            cursor.execute("INSERT INTO weather (temperature_c, r_humidity) VALUES ('20.8', '65');")
            conn.commit()

if __name__ == "__main__":
    configuring_a_sample_sqlite_database()
    APIGen = APIGenerator(showLogs=True)
    APIGen.load_ontologies(paths=[
        "metadata_example.ttl",
        "bm_example.ttl"
    ])
    APIGen.serialize_ontologies()
    api_app = APIGen.generate_api_routes()
    uvicorn.run(api_app, host="127.0.0.1", port=5000)