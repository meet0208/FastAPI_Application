from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
from Todos.models import Todos, Users
import pytest
from ..Router.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Wherever you're setting up your test DB
# Base.metadata.drop_all(bind=engine)  # Optional, to clean old tables
Base.metadata.create_all(bind=engine)

# Base.metadata.create_all(bind=engine)

def override_get_current_user():
    return {'username': 'testadmin', 'id': 1, 'user_role': 'admin'}

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn fatsapi",
        description = "Learn fatsapi",
        priority = 1,
        complete= False,
        owner_id = 1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    """ 
    "return todo" 'If we use this than the code written below to delete the created data in the todo table will never executes, as return doesn't
    allow to complete the task whereas if we use yield than it doesn't stop until all the task gets complete related to the todo.
    """
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()

@pytest.fixture
def test_user():
    user = Users(
        username = "testadmin",
        email = "meet123@gmail.com",
        first_name = "meet",
        last_name = "boghani",
        hashed_password = bcrypt_context.hash("testpassword"),
        role = "admin",
        phone_number = "2631111111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()