from .utils import *
from ..Router.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testadmin"
    assert response.json()["email"] == "meet123@gmail.com"
    assert response.json()["first_name"] == "meet"
    assert response.json()["last_name"] == "boghani"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "2631111111"

def test_change_password_success(test_user):
    response = client.put("/user/change_password/", json={"password": "testpassword", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_fail(test_user):
    response = client.put("/user/change_password/", json={"password": "testpassword12", "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'error on password change.'}

def test_change_phone_number(test_user):
    response = client.put("/user/phone_number/1234567890")
    assert response.status_code == status.HTTP_204_NO_CONTENT