from sqlalchemy.ext.asyncio import AsyncSession
from repository.user_repository import UserRepository
from views.user_schema import UserCreate

class UserService:
    @staticmethod
    async def get_users(db: AsyncSession):
        return await UserRepository.get_all_users(db)

    @staticmethod
    async def create_user(user_data: UserCreate, db: AsyncSession):
        return await UserRepository.create_user(db, user_data)
