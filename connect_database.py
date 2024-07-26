from db_secrets import secrets 
from sqlalchemy import create_engine
import pandas as pd

db_name = "MovieDB"
db_user = secrets.get('DATABASE_USER')
db_password = secrets.get('DATABASE_PASSWORD')
db_port = secrets.get('DATABASE_PORT')
db_host = 'localhost'

def insert_df_to_table(df):
    engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    df.to_sql('reviews', engine, if_exists='replace', index=False)
