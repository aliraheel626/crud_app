from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
 
engine = create_async_engine("sqlite+aiosqlite:///./test.db", echo=True)



# dependency
async def get_db():
    async with AsyncSession(bind=engine) as session:
        yield session
    print('session closed')