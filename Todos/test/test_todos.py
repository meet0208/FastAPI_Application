from typing import Annotated
import pytest
# from Todos.Router.auth import get_db
from httpcore import request
from ..Router.todos import get_db, get_current_user
from fastapi import status, Depends
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': "Learn fatsapi", 'description': "Learn fatsapi", 'priority': 1, 'id':1, 'owner_id': 1}]

def test_read_one_authenticated(test_todo):
    response = client.get('/todos/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': "Learn fatsapi", 'description': "Learn fatsapi", 'priority': 1, 'id':1, 'owner_id': 1}

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
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "New todo updated"

def test_delete_todo(test_todo):
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None