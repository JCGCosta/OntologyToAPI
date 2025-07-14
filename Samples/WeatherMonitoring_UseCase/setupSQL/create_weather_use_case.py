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
with open("weather_SQL_database.sql", "r") as file:
    sql_script = file.read()

commands = [cmd.strip() for cmd in sql_script.split(";") if cmd.strip()]

conn = engine.connect()
transaction = conn.begin()
for command in commands:
    conn.execute(text(command))
transaction.commit()
conn.close()
print("Database and schema created successfully.")
