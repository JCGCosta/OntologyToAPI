from sqlalchemy import create_engine, text
import pandas as pd
from Settings import auto_config as cfg

username = cfg.MYSQL_USERNAME
password = cfg.MYSQL_PASSWORD
host = cfg.MYSQL_IP_ADDRESS
port = cfg.MYSQL_PORT

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/")

print(f"Connected to {host}:{port} with the following credentials: {username}:{password}.")

# Read and execute the SQL file
with open("pb_lem_SQL_database.sql", "r") as file:
    sql_script = file.read()

commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]

conn = engine.connect()
transaction = conn.begin()
for command in commands:
    conn.execute(text(command))
transaction.commit()
conn.close()
print("Database and schema created successfully.")

df = pd.read_csv("Datasets/AggregatedUseCase.csv", sep="\t")
df.columns = ["MEMBER_ID", "UTC_T", "ELECTRICITY_LOAD", "RESIDENTIAL_ELECTRICITY_PRICE", "RESIDENTIAL_SOLAR_GENERATION",
    "RESIDENTIAL_WIND_GENERATION", "TEMPERATURE", "RELATIVE_HUMIDITY"]

df["UTC_T"] = pd.to_datetime(df["UTC_T"], format="%d/%m/%Y %H:%M")

def insertSimulation(row, conn):
    # Prepare SQL statement with placeholders
    sql = text("""
        INSERT INTO LEM_DATA (
            MEMBER_ID, UTC_T, ELECTRICITY_LOAD, RESIDENTIAL_ELECTRICITY_PRICE,
            RESIDENTIAL_SOLAR_GENERATION, RESIDENTIAL_WIND_GENERATION,
            TEMPERATURE, RELATIVE_HUMIDITY
        ) VALUES (
            :member_id, :utc_t, :electricity_load, :price,
            :solar_gen, :wind_gen, :temp, :humidity
        )
    """)

    # Map DataFrame row to parameters
    params = {
        "member_id": row["MEMBER_ID"],
        "utc_t": row["UTC_T"],
        "electricity_load": row["ELECTRICITY_LOAD"],
        "price": row["RESIDENTIAL_ELECTRICITY_PRICE"],
        "solar_gen": row["RESIDENTIAL_SOLAR_GENERATION"],
        "wind_gen": row["RESIDENTIAL_WIND_GENERATION"],
        "temp": row["TEMPERATURE"],
        "humidity": row["RELATIVE_HUMIDITY"]
    }

    conn.execute(sql, params)

# Use a single connection and transaction for all rows
with engine.begin() as conn:
    df.apply(insertSimulation, axis=1, args=(conn,))

print("LEM Scenario inserted into the database.")
