import pytest
from fastapi.testclient import TestClient

from src.main import app
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.exceptions import *
from src.db import Base

client = TestClient(app=app)

@pytest.fixture(scope='function')
async def setup_database(get_session: AsyncSession):
    # Create tables in the test database
    async with get_session.bind.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Optionally, drop tables after tests
    async with get_session.bind.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

def test_register_success(get_session: AsyncSession, setup_database, override_get_session):
    response = client.post(
        url="/auth/register",  # Use relative URL since TestClient handles the base URL
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "first_name": "Kanat",
            "last_name": "Zhetru",
            "email": "Kanat123@gmail.com",
            "password": "test123!",
            "password_confirm": "test123!"
        }
    )
    response.status_code == 201, f"Expected status code 201, got {response.status_code}"

 
def test_register_email_exists(setup_database, override_get_session):
    # First, register a user
    response = client.post(
        url="/auth/register",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "first_name": "Kanat",
            "last_name": "Zhetru",
            "email": "Kanat123@gmail.com",
            "password": "test123!",
            "password_confirm": "test123!"
        }
    )
    response = client.post(
            url="/auth/register",
            headers={"accept": "application/json", "Content-Type": "application/json"},
            json={
                "first_name": "Kanat",
                "last_name": "Zhetru",
                "email": "Kanat123@gmail.com",
                "password": "test123!",
                "password_confirm": "test123!"
            }
        )
    assert response.status_code == 409
    assert response.json()["message"] == "Successfully registered"



def test_register_password_does_not_match():
    with pytest.raises(PasswordDoesNotMatchException):
        client.post(url="http://localhost:8003/auth/register",
                    headers={"accept": "application/json",
                             "Content-Type": "application/json"},
                             data='{ \
                                  "first_name": "Kanat",\
                                  "last_name": "Zhetru",\
                                  "email": "Kanat123@gmail.com",\
                                  "password": "test123!",\
                                  "password_confirm": "te"\
                                }')

def test_login():
    response = client.post(url="http://localhost:8003/auth/login",
                headers={"accept": "application/json",
                         "Content-Type": "application/x-www-form-urlencoded"},
                         data="grant_type=password&username=Kanat123%40gmail.com&password=test123!&scope=&client_id=string&client_secret=********")
    access_token = response.cookies.get('access_token')
    refresh_token = response.cookies.get('refresh_token')
    token = response.json()
    
    
    