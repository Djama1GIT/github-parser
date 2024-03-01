from asyncpg import create_pool

from config import Settings


async def get_db_pool():
    settings = Settings()
    pool = await create_pool(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
        host=settings.POSTGRES_HOST,
    )
    try:
        yield pool
    finally:
        await pool.close()
