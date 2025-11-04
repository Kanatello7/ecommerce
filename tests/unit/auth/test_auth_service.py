import pytest
from pytest_mock import MockerFixture
from datetime import datetime,  timedelta

from src.auth.service import AuthService
from src.auth.schemas import UserRegister, Token
from src.auth.exceptions import UserExistsException, PasswordDoesNotMatchException, InvalidTokenException
from src.auth.config import settings_jwt

@pytest.fixture
def fixed_utc_time():
    return datetime(2025, 10, 10, 10, 10, 0)

@pytest.mark.unit
async def test_authenticate_user_success(mocker: MockerFixture, sample_user):
    mock_user_service = mocker.Mock()
    mock_user_service.get_user_by_username = mocker.AsyncMock(return_value=sample_user)
    mock_auth_repo = mocker.Mock()  
    mock_verify = mocker.patch("src.auth.service.verify_password", return_value=True)  # Mock verify_password
    
    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)
    
    result = await auth_service.authenticate_user(username="tom@gmail.com", password="plain_password")
    
    mock_user_service.get_user_by_username.assert_called_once_with("tom@gmail.com")
    assert result == sample_user
    assert result.email == "tom@gmail.com"
    mock_verify.assert_called_once_with("plain_password", "hashed_password")

@pytest.mark.unit 
async def test_authenticate_user_fail(mocker: MockerFixture):
    mock_user_service = mocker.Mock()
    mock_user_service.get_user_by_username = mocker.AsyncMock(return_value=None)
    mock_auth_repo = mocker.Mock()  

    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)

    result = await auth_service.authenticate_user("notexist@gmail.com", password="plain_password")
    
    mock_user_service.get_user_by_username.assert_called_once_with("notexist@gmail.com")
    assert result == False

@pytest.mark.unit 
async def test_authenticate_user_wrong_password(mocker: MockerFixture, sample_user):
    mock_user_service = mocker.Mock()
    mock_user_service.get_user_by_username = mocker.AsyncMock(return_value=sample_user)
    mock_auth_repo = mocker.Mock()  
    mocker_verify = mocker.patch("src.auth.service.verify_password", return_value=False)

    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)

    result = await auth_service.authenticate_user("tom@gmail.com", password="wrong_password")
    
    mock_user_service.get_user_by_username.assert_called_once_with("tom@gmail.com")
    assert result == False
    mocker_verify.assert_called_once_with("wrong_password", "hashed_password")

@pytest.mark.unit 
async def test_create_access_token(mocker: MockerFixture, sample_user, fixed_utc_time):
    mock_user_service = mocker.Mock()
    mock_auth_repo = mocker.Mock()
    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)
    
    mocker.patch("src.auth.service.get_utc_now", return_value=fixed_utc_time)
    mock_jwt_encode = mocker.patch("jwt.encode", return_value="mocked_access_token")

    expected_payload = {
        "sub": sample_user.email,
        "type": "access", 
        "iat": fixed_utc_time,
        "exp": fixed_utc_time + timedelta(minutes=settings_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    access_token = await auth_service.create_access_token(sample_user)
    mock_jwt_encode.assert_called_once_with(expected_payload, settings_jwt.SECRET_KEY, algorithm=settings_jwt.ALGORITHM)
    
    assert access_token == "mocked_access_token"


@pytest.mark.unit 
async def test_create_refresh_token(mocker: MockerFixture, sample_user, fixed_utc_time):
    mock_user_service = mocker.Mock()
    mock_auth_repo = mocker.Mock()
    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)
    
    mocker.patch("src.auth.service.get_utc_now", return_value=fixed_utc_time)
    mock_jwt_encode = mocker.patch("jwt.encode", return_value="mocked_refresh_token")

    expected_payload = {
        "sub": sample_user.email,
        "type": "refresh", 
        "iat": fixed_utc_time,
        "exp": fixed_utc_time + timedelta(days=settings_jwt.REFRESH_TOKEN_EXPIRE_DAYS)
    }

    access_token = await auth_service.create_refresh_token(sample_user)
    mock_jwt_encode.assert_called_once_with(expected_payload, settings_jwt.SECRET_KEY, algorithm=settings_jwt.ALGORITHM)
    
    assert access_token == "mocked_refresh_token"

@pytest.mark.unit 
async def test_create_token_pair(mocker: MockerFixture, sample_user, fixed_utc_time):
    mock_user_service = mocker.AsyncMock()
    mock_auth_repo = mocker.AsyncMock()
    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)

    mock_user_service.set_login_time.return_value=fixed_utc_time
    mocker.patch.object(
        auth_service,
        "create_access_token",
        new=mocker.AsyncMock(return_value="mocked_access_token")
    )

    
    mocker.patch.object(
        auth_service,
        "create_refresh_token",
        new=mocker.AsyncMock(return_value="mocked_refresh_token")
    )

    token = await auth_service.create_token_pair(sample_user)

    auth_service.create_access_token.assert_called_once_with(sample_user)
    auth_service.create_refresh_token.assert_called_once_with(sample_user)
    mock_user_service.set_login_time.assert_called_once_with(sample_user)
    assert token.access_token == "mocked_access_token"
    assert token.refresh_token == "mocked_refresh_token"
    assert token.token_type == 'bearer'

@pytest.mark.unit
async def test_register_new_user_success(mocker: MockerFixture, sample_user):
    mock_auth_repo = mocker.Mock()
    mock_user_service = mocker.Mock()
    mock_user_service.get_user_by_username = mocker.AsyncMock(return_value=None)
    mock_user_service.create_new_user = mocker.AsyncMock(return_value=sample_user)

    mocker_hash = mocker.patch("src.auth.service.hash_password", return_value="hashed_password")

    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)
    new_user_data = UserRegister(first_name="tom", last_name="holland", email="tom@gmail.com",
                                  password="plain_password", password_confirm="plain_password")    
    
    expected_data = {
        "first_name": "tom",
        "last_name": "holland",
        "email": "tom@gmail.com",
        "password": "hashed_password"
    }

    result = await auth_service.register_new_user(new_user_data)

    mock_user_service.get_user_by_username.assert_called_once_with("tom@gmail.com")
    mock_user_service.create_new_user.assert_called_once_with(expected_data)
    mocker_hash.assert_called_once_with("plain_password")
    assert result == sample_user
    assert result.email == "tom@gmail.com"

@pytest.mark.unit
async def test_register_new_user_user_exists(mocker: MockerFixture, sample_user):
    mock_auth_repo = mocker.Mock()
    mock_user_service = mocker.Mock()
    mock_user_service.get_user_by_username = mocker.AsyncMock(return_value=sample_user)

    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)
    new_user_data = UserRegister(first_name="tom", last_name="holland", email="tom@gmail.com",
                                  password="plain_password", password_confirm="plain_password")    

    with pytest.raises(UserExistsException):
        result = await auth_service.register_new_user(new_user_data)

    mock_user_service.get_user_by_username.assert_called_once_with("tom@gmail.com")
   
@pytest.mark.unit
async def test_register_new_user_password_mismatch(mocker: MockerFixture):
    mock_auth_repo = mocker.Mock()
    mock_user_service = mocker.Mock()
    mock_user_service.get_user_by_username = mocker.AsyncMock(return_value=None)
    
    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)
    new_user_data = UserRegister(first_name="tom", last_name="holland", email="tom@gmail.com",
                                  password="plain_password", password_confirm="mismatch_password")    
    
    with pytest.raises(PasswordDoesNotMatchException):
        result = await auth_service.register_new_user(new_user_data)

    mock_user_service.get_user_by_username.assert_called_once_with("tom@gmail.com")

@pytest.mark.unit 
@pytest.mark.parametrize(("type", "exp_minutes"), [
    ("access", settings_jwt.ACCESS_TOKEN_EXPIRE_MINUTES),
    ("refresh", settings_jwt.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60),
])
async def test_decode_token(mocker: MockerFixture, fixed_utc_time, type, exp_minutes):
    payload = {
        "sub": "tom@gmail.com",
        "type": type,
        "iat": fixed_utc_time,
        "exp": fixed_utc_time + timedelta(minutes=exp_minutes)
    }

    mock_repo = mocker.Mock()
    mock_user_service = mocker.Mock()
    mock_jwt_decode = mocker.patch("jwt.decode", return_value=payload)

    auth_service = AuthService(repository=mock_repo, user_service=mock_user_service)
    result = await auth_service.decode_token(f"{type}_token")

    mock_jwt_decode.assert_called_once_with(f"{type}_token", settings_jwt.SECRET_KEY, algorithms=[settings_jwt.ALGORITHM])
    assert result == payload

@pytest.mark.unit 
async def test_refresh_success(mocker: MockerFixture, sample_user, fixed_utc_time):
    payload = {
        "sub": "tom@gmail.com",
        "type": "refresh",
        "iat": fixed_utc_time,
        "exp": fixed_utc_time + timedelta(days=settings_jwt.REFRESH_TOKEN_EXPIRE_DAYS)
    }
    mock_auth_repo = mocker.Mock()
    mock_user_service = mocker.Mock()
    mock_user_service.get_user_by_username = mocker.AsyncMock(return_value=sample_user)

    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)
    mocker.patch.object(
        auth_service,
        "decode_token",
        new=mocker.AsyncMock(return_value=payload)
    )
    mocker.patch.object(
        auth_service,
        "create_token_pair",
        new= mocker.AsyncMock(return_value=Token(access_token="new_access_token",
                                                                              refresh_token="new_refresh_token",
                                                                              token_type="bearer"))
    )
    result = await auth_service.refresh_token("refresh_token")

    auth_service.decode_token.assert_called_once_with("refresh_token")
    mock_user_service.get_user_by_username.assert_called_once_with("tom@gmail.com")
    auth_service.create_token_pair.assert_called_once_with(sample_user)
    assert result.access_token == "new_access_token"
    assert result.refresh_token == "new_refresh_token"
    assert result.token_type == "bearer"
    
@pytest.mark.unit
async def test_refresh_invalid_token(mocker: MockerFixture, fixed_utc_time):
    payload = {
        "type": "refresh",
        "iat": fixed_utc_time,
        "exp": fixed_utc_time + timedelta(days=settings_jwt.REFRESH_TOKEN_EXPIRE_DAYS)
    }
    mock_auth_repo = mocker.Mock()
    mock_user_service = mocker.Mock()
    
    auth_service = AuthService(repository=mock_auth_repo, user_service=mock_user_service)
    mocker.patch.object(
        auth_service,
        "decode_token",
        new=mocker.AsyncMock(return_value=payload)
    )

    with pytest.raises(InvalidTokenException):
        result = await auth_service.refresh_token("refresh_token")
    
    auth_service.decode_token.assert_called_once_with("refresh_token")

