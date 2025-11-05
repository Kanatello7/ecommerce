import pytest 
from pytest_mock import MockerFixture

from src.auth.service import UserService

@pytest.mark.unit 
async def test_get_user_by_username_success(mocker: MockerFixture, sample_user):
    mock_repo = mocker.Mock()
    mock_repo.find_one_or_many = mocker.AsyncMock(return_value=[sample_user])
    user_service = UserService(mock_repo)

    result = await user_service.get_user_by_username(username='tom@gmail.com')

    mock_repo.find_one_or_many.assert_called_once_with(email="tom@gmail.com")
    assert result == sample_user
    assert result.email == "tom@gmail.com"

@pytest.mark.unit 
async def test_get_user_by_username_not_exist(mocker: MockerFixture, sample_user):
    mock_repo = mocker.Mock()
    mock_repo.find_one_or_many = mocker.AsyncMock(return_value=None)
    user_service = UserService(mock_repo)

    result = await user_service.get_user_by_username(username="notexist@gmail.com")

    mock_repo.find_one_or_many.assert_called_once_with(email="notexist@gmail.com")
    assert result is None

@pytest.mark.unit
async def test_create_new_user(mocker: MockerFixture, sample_user, sample_user_data):
    mock_repo = mocker.Mock()
    mock_repo.create = mocker.AsyncMock(return_value=sample_user)
    user_service = UserService(mock_repo)

    result = await user_service.create_new_user(sample_user_data)
    
    mock_repo.create.assert_called_once_with(sample_user_data)
    assert result == sample_user
    assert result.email == "tom@gmail.com"

