import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv('credentials.env')
passwd = os.environ.get('PASSWD')

SQLALCHEMY_DATABASE_URI = f'mysql://root:{passwd}@localhost/pokemon_db'

Base = declarative_base()

engine = create_engine(SQLALCHEMY_DATABASE_URI)

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
