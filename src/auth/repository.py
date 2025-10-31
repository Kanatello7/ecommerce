from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.cart.models import Cart
from src.utils import SqlAlchemyCRUDRepository
from datetime import datetime, timezone

class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session 

class UserRepository(SqlAlchemyCRUDRepository):
    model = User

    async def set_login_time(self, user: User):
        user.last_login = datetime.now(tz=timezone.utc)
        await self.session.commit()