# Imports
import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()
db_host = os.getenv('db_host')
db_name = os.getenv('db_db')
db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
db_port = os.getenv('db_port')

print(db_host, db_name, db_user, db_pass, db_port); 

uri = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
alchemyEngine=create_engine(uri)

# Query
q = """SELECT * FROM information_schema"""

dbConnection = alchemyEngine.connect(); 

df=pd.read_sql(q, dbConnection); # Pulling data

print(df.head())