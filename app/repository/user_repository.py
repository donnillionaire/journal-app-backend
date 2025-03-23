from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User

class UserRepository:
    @staticmethod
    async def get_all_users(db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def create_user(db: AsyncSession, user_data):
        user = User(name=user_data.name, email=user_data.email)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
