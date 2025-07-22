from contextlib import asynccontextmanager

from fastapi import FastAPI

from controllers import auth, post
from src.database import database, engine, metadata


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    await database.connect()
    yield
    # Shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(post.router)
app.include_router(auth.router)
