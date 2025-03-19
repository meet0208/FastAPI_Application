from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


"""
This is used to connect database with local database which is sqlite3.
"""
    # SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
"""
This crededbtials is to connect postgresql which is server based swl database. 
"""
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL) # connect_args={'check_same_thread': False} this parameter is used only for sqlite3
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()