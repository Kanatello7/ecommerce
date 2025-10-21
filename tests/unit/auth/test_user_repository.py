import pytest 

from src.auth.repository import UserRepository
from src.auth.models import User

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

@pytest.mark.unit 
async def test_find_or_more_success(test_user_repository: UserRepository, get_session: AsyncSession):
    user = User(id=1, first_name="tom", last_name="holland", email="tom@gmail.com", password="hashed_password")
    get_session.add(user)
    await get_session.commit() 

    result = await test_user_repository.find_one_or_more(email="tom@gmail.com")

    assert result.email == "tom@gmail.com"

@pytest.mark.unit
async def test_find_or_more_not_exists(test_user_repository: UserRepository):
    result = await test_user_repository.find_one_or_more(email="tom@gmail.com")

    assert result is None

@pytest.mark.unit
async def test_create(test_user_repository: UserRepository, get_session: AsyncSession):
    user_data = {"id": 1, "first_name": "tom", "last_name": "holland", "email": "tom@gmail.com", "password": "hashed_password"}

    result = await test_user_repository.create(user_data)

    assert result.email == "tom@gmail.com"
    query = select(User).filter_by(email="tom@gmail.com")
    db_result = await get_session.execute(query)
    
    assert db_result.scalar_one().email == "tom@gmail.com"