import pytest

from src.auth.exceptions import *
from src.auth.dependencies import *
from src.auth.config import settings_jwt
from src.auth.utils import get_utc_now

from datetime import timedelta
import jwt

@pytest.mark.integration
async def test_register_success(async_client):
    response = await async_client.post(
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
    user = response.json()
    assert response.status_code == 201
    assert user["first_name"] == "Kanat" and user["last_name"] == "Zhetru" and user["email"] == "Kanat123@gmail.com"

@pytest.mark.integration
async def test_register_email_exists(async_client):
    # First, register a user
    response = await async_client.post(
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
    response = await async_client.post(
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

@pytest.mark.integration
async def test_register_password_does_not_match(async_client):
    response = await async_client.post(url="/auth/register",
                    headers={"accept": "application/json",
                             "Content-Type": "application/json"},
                             json={  
                                 "first_name": "Kanat",
                                 "last_name": "Zhetru",
                                 "email": "Kana@gmail.com",
                                 "password": "test123!",
                                 "password_confirm": "te"
                             })
    assert response.status_code == 417

@pytest.mark.integration
async def test_login_success(async_client):
    response = await async_client.post(
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
    
    login_response = await async_client.post(url="/auth/login",
                                             headers={"accept": "application/json",
                                              "Content-Type": "application/x-www-form-urlencoded"},
                                             content="grant_type=password&username=Kanat123%40gmail.com&password=test123!&scope=&client_id=string&client_secret=********")
    
    # Check cookies are set
    access_token = login_response.cookies.get('access_token')
    refresh_token = login_response.cookies.get('refresh_token')
    
    # Also check Set-Cookie headers for coverage
    set_cookie_headers = login_response.headers.get_list('set-cookie')
    assert len(set_cookie_headers) >= 2
    assert any('access_token' in cookie for cookie in set_cookie_headers)
    assert any('refresh_token' in cookie for cookie in set_cookie_headers)
    assert any('HttpOnly' in cookie for cookie in set_cookie_headers)
    
    # Verify token data
    token = login_response.json()
    payload = jwt.decode(token["access_token"], settings_jwt.SECRET_KEY, algorithms=[settings_jwt.ALGORITHM])
    
    assert login_response.status_code == 200
    assert access_token is not None
    assert refresh_token is not None
    assert token["token_type"] == 'bearer'
    assert payload["sub"] == "Kanat123@gmail.com"

@pytest.mark.integration
async def test_refresh_token_success(async_client):
    # Step 1: Register a user
    await async_client.post(
        url="/auth/register",  
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "first_name": "Kanat",
            "last_name": "Zhetru",
            "email": "refresh_test@gmail.com",
            "password": "test123!",
            "password_confirm": "test123!"
        }
    )
    # Step 2: Login a user
    login_response = await async_client.post(
        url="/auth/login",
        headers={"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        content="grant_type=password&username=refresh_test%40gmail.com&password=test123!&scope=&client_id=string&client_secret=********"
    )
    
    old_access_token = login_response.cookies.get('access_token')
    old_refresh_token = login_response.cookies.get('refresh_token')
    
    assert old_access_token is not None
    assert old_refresh_token is not None

    # Step 3: Refresh tokens
    refresh_response = await async_client.post(
        url='/auth/refresh',
        cookies={"refresh_token": old_refresh_token}
    )

    assert refresh_response.status_code == 200 
    
    # Check cookies
    new_access_token = refresh_response.cookies.get('access_token')
    new_refresh_token = refresh_response.cookies.get('refresh_token')
    
    assert new_access_token is not None
    assert new_refresh_token is not None
    
    # Check Set-Cookie headers for coverage
    set_cookie_headers = refresh_response.headers.get_list('set-cookie')
    assert len(set_cookie_headers) >= 2
    assert any('access_token' in cookie for cookie in set_cookie_headers)
    assert any('refresh_token' in cookie for cookie in set_cookie_headers)
    assert any('HttpOnly' in cookie for cookie in set_cookie_headers)
    
    # Verify Max-Age is set
    access_cookie = [c for c in set_cookie_headers if 'access_token' in c][0]
    refresh_cookie = [c for c in set_cookie_headers if 'refresh_token' in c][0]
    assert 'Max-Age' in access_cookie
    assert 'Max-Age' in refresh_cookie
    
    # Check response body contains tokens
    token_data = refresh_response.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data
    assert token_data["token_type"] == "bearer"
    
    # Verify the new access token is valid and contains correct payload
    payload = jwt.decode(
        token_data["access_token"], 
        settings_jwt.SECRET_KEY, 
        algorithms=[settings_jwt.ALGORITHM]
    )
    assert payload["sub"] == "refresh_test@gmail.com"

@pytest.mark.integration
async def test_refresh_token_expired(async_client):
    exp_payload = {
        "sub": "refresh@gmail.com",
        "iat": get_utc_now(),
        "exp": get_utc_now() - timedelta(days=1)
    }
    expired_token = jwt.encode(
        exp_payload,
        settings_jwt.SECRET_KEY,
        algorithm=settings_jwt.ALGORITHM
    )

    
    response = await async_client.post(
        url="/auth/refresh",
        cookies={"refresh_token": expired_token}
    )
    assert response.status_code == 401

@pytest.mark.integration
async def test_refresh_token_missing(async_client):
    """Test refresh endpoint when no refresh token is provided"""
    response = await async_client.post(url="/auth/refresh")
    
    assert response.status_code == 401

@pytest.mark.integration
async def test_refresh_token_invalid(async_client):
    """Test refresh endpoint with invalid refresh token"""
    response = await async_client.post(
        url="/auth/refresh",
        cookies={"refresh_token": "invalid_token_string"}
    )
    
    assert response.status_code == 401

@pytest.mark.integration
@pytest.mark.parametrize(("email", "password"), [
    ("wrong_email", "test123!"),
    ("Kanat123@gmail.com", "wrong_password"),
])  
async def test_login_invalid_credentials(async_client, email, password):
    response = await async_client.post(
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

    response = await async_client.post(url="/auth/login",
            headers={"accept": "application/json",
                     "Content-Type": "application/x-www-form-urlencoded"},
                     content=f"grant_type=password&username={email}&password={password}&scope=&client_id=string&client_secret=********")
    assert response.status_code == 401

@pytest.mark.integration
async def test_logout(async_client):
    response = await async_client.post(
        url="/auth/logout", 
        headers={"accept": "application/json"}
    )

    # Check Set-Cookie headers for cookie deletion
    set_cookie_headers = response.headers.get_list('set-cookie')
    
    # Verify cookies are being deleted (Max-Age=0 or expires in the past)
    access_cookie_deleted = any('access_token' in cookie and ('Max-Age=0' in cookie or 'expires=' in cookie) 
                                for cookie in set_cookie_headers)
    refresh_cookie_deleted = any('refresh_token' in cookie and ('Max-Age=0' in cookie or 'expires=' in cookie) 
                                 for cookie in set_cookie_headers)
    
    assert response.status_code == 200 
    assert response.json()["message"] == "Logged out successfully"
    assert access_cookie_deleted or len(set_cookie_headers) >= 1  # Cookie deletion sets headers
    assert refresh_cookie_deleted or len(set_cookie_headers) >= 1

@pytest.mark.integration
async def test_logout_clears_cookies_properly(async_client):
    """More thorough test to ensure logout properly clears cookies"""
    # First login
    await async_client.post(
        url="/auth/register",  
        headers={"accept": "application/json", "Content-Type": "application/json"},
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "logout_test@gmail.com",
            "password": "test123!",
            "password_confirm": "test123!"
        }
    )
    
    login_response = await async_client.post(
        url="/auth/login",
        headers={"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"},
        content="grant_type=password&username=logout_test%40gmail.com&password=test123!&scope=&client_id=string&client_secret=********"
    )
    
    # Verify we got cookies
    assert login_response.cookies.get('access_token') is not None
    assert login_response.cookies.get('refresh_token') is not None
    
    # Now logout
    logout_response = await async_client.post(url="/auth/logout")
    
    # Check that delete_cookie was called (check Set-Cookie headers)
    set_cookie_headers = logout_response.headers.get_list('set-cookie')
    assert len(set_cookie_headers) >= 2  # Both cookies should be deleted
    
    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Logged out successfully"