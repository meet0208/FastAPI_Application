from typing import Annotated

import pytest
from Todos.Router.auth import get_db
from Todos.models import Todos
from httpcore import request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..Router.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status, Depends

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# dp_dependency = Annotated[Session, Depends(override_get_db)]

def override_get_current_user():
    return {'username': 'admin', 'id': 4, 'user_role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn fatsapi",
        description = "Learn fatsapi",
        priority = 1,
        complete= False,
        owner_id = 4,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    """ 
    return todo 'If we use this than the code wrigtten below to delete the created data in the todo table will never execute as return doesn't
    allow to complete the task whereas if we use yield than it doesn't stop until all the task gets complete related to the todo.
    """
    yield todo
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()


def test_read_all_authenticated(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': "Learn fatsapi", 'description': "Learn fatsapi", 'priority': 1, 'id':1, 'owner_id': 4}]

def test_read_one_authenticated(test_todo):
    response = client.get('/todos/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': "Learn fatsapi", 'description': "Learn fatsapi", 'priority': 1, 'id':1, 'owner_id': 4}

def test_read_one_not_authenticated():
    response = client.get('/todos/20')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Data not found'}

def test_create_todo(test_todo):
    request_data = {
        'title': 'New todo',
        'description': 'Learn new todo',
        'priority': 1,
        'complete': False,
    }

    response = client.post('/todos', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo(test_todo):
    request_data = {
        'title': 'New todo updated',
        'description': 'Learn new todo updated',
        'priority': 5,
        'complete': True,
    }

    response = client.put('/todos/1',json = request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_todo(test_todo):
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None