import asyncio
from beanie.executors.migrate import run_migrate, MigrationSettings, RunningDirections
from settings.config import settings


async def migrate():
    await run_migrate(
        settings=MigrationSettings(
            direction=RunningDirections.BACKWARD,
            connection_uri=f'mongodb://{settings.MONGODB_USER}:{settings.MONGODB_PASSWORD}@{settings.MONGODB_HOST}',
            database_name=settings.MONGODB_DB,
            path='src/infrastructure/migrations/',
        )
    )

if __name__ == "__main__":
    asyncio.run(migrate())
