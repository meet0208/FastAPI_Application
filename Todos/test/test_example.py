import pytest

def test_equal_not_equal():
    assert 9 == 9

def test_boolean():
    assert ("hello" == "hello") is True

def test_instance():
    assert isinstance("hello", str)
    assert not isinstance("hello", int)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student("John", "Doe", "computer science", 3)

def test_person_initialization(default_employee):
    assert default_employee.first_name == "John", 'First name should be John'
    assert default_employee.last_name == "Doe", 'Last name should be Doe'
    assert default_employee.major == "computer science", 'Major should be computer science'
    assert default_employee.years == 3, 'Years should be 3'