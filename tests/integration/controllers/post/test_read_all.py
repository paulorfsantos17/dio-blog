import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient


@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
    from schemas.post import PostIn
    from src.services.post import PostService

    service = PostService()
    await service.create_post(PostIn(title="test", content="test", published=True))
    await service.create_post(PostIn(title="test2", content="test2", published=True))
    await service.create_post(PostIn(title="test3", content="test3", published=False))


@pytest.mark.parametrize("published, total", [(True, 2), (False, 1)])
async def test_read_all_posts_by_status_success(client: AsyncClient, access_token: str, published: bool, total: int):
    # Given
    params = {
        "published": published,
        "limit": 10
    }
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # When
    response = await client.get("/posts/", params=params, headers=headers)

    # Then
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == total


async def test_read_posts_empty_parameters_fail(client: AsyncClient, access_token: str):
    # Given
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # When
    response = await client.get("/posts/", headers=headers)

    # Then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    
async def test_read_all_post_not_autheticated_fail(client: AsyncClient):
    #Given
    params = {
        "published": True,
        "limit": 10
    }
    
    #When
    response = await client.get("/posts/", params=params)
    
    #Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    