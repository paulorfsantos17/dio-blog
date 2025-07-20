from contextlib import asynccontextmanager

from fastapi import FastAPI

from controllers import auth, post
from database import database, engine, metadata


@asynccontextmanager
async def lifespan(app: FastAPI):
    from models.post import posts  # noqa

    # Startup
    await database.connect()
    metadata.create_all(engine)
    yield
    # Shutdown
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
# Conectar/desconectar ao banco


app.include_router(post.router)
app.include_router(auth.router)
