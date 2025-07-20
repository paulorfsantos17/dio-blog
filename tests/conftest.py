import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

@pytest_asyncio.fixture
async def db():
    from src.database import database, engine, metadata
    from src.models.post import posts  # noqa: import para registrar a tabela

    await database.connect()
    metadata.create_all(engine)

    yield  # 👈 Aguarda o teste

    await database.disconnect()
    metadata.drop_all(engine)


@pytest_asyncio.fixture
async def client(db):
    from src.main import app

    transport = ASGITransport(app=app)  # corrigido nome
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    async with AsyncClient(base_url="https://test", transport=transport, headers=headers) as client:
        yield client


@pytest_asyncio.fixture
async def acess_token(client: AsyncClient):
    response = await client.post("/auth/login", json={"user_id": 1})
    return response.json()["access_token"]
