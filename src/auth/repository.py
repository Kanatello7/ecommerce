from sqlalchemy.ext.asyncio import AsyncSession

class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session 

class UserRepository:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model 

    async def find_one_or_more()