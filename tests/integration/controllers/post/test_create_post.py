from fastapi import status
from httpx import AsyncClient


async def test_create_post_success(client: AsyncClient, acess_token: str):
  #Given
  headers = {
    "Authorization": f"Bearer {acess_token}"
  }
  
  data = {
    "title": "test",
    "content": "test",
    "published": True
  }
  
  #When
  response = await client.post("/posts/", json=data, headers=headers)
  
  #Then
  content = response.json()
  
  assert response.status_code == status.HTTP_201_CREATED
  assert content["id"] is not None
  
async def test_create_post_fail(client: AsyncClient, acess_token: str):
  #Given
  headers = {
    "Authorization": f"Bearer {acess_token}"
  }
  
  data = {
    "content": "test"
  }
  
  #When
  response = await client.post("/posts/", json=data, headers=headers)
  
  #Then
  content = response.json()
  
  assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
  assert content["detail"][0]["loc"] == ["body", "title"]
  
async def test_create_post_not_autheticated_fail(client: AsyncClient):
    #Given
    data = {
      "title": "test",
      "content": "test",
      "published": True
    }
    
    #When
    response = await client.post("/posts/", json=data)
    
    #Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED