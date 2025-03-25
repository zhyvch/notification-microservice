from contextlib import asynccontextmanager

from fastapi import FastAPI

from settings.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await init_db()
    yield


def create_app():
    app = FastAPI(
        title='Notification Service',
        description='Simple notification service',
        docs_url='/api/docs',
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    # app.include_router(router, prefix='/notifications')

    return app