from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


"""
This is used to connect database with local database which is sqlite3.
"""
    # SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
    # engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

"""
This crededbtials is to connect postgresql which is server based sql database. 
"""
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/TodoApplicationDatabase'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

"""
This crededbtials is to connect postgresql on render as Paas(project as a service).
"""
SQLALCHEMY_DATABASE_URL = 'postgresql://todoapplicationdatabase_99sq_user:yvpq5ff30UnWhk9ic0uHBEkffpFDqjNn@dpg-d0hcmkidbo4c73dld8u0-a.oregon-postgres.render.com/todoapplicationdatabase_99sq'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()