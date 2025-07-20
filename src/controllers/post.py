from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer

from schemas.post import PostIn, PostUpdate
from security import verify_token, verify_token_valid
from services.post import PostService
from views.post import PostOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # define a URL de login para docs


# No APIRouter, você usa essa dependência global:
router = APIRouter(
    prefix="/posts",
    dependencies=[Depends(verify_token_valid)]  # vai exigir token válido no header Authorization
)
service = PostService()


@router.get("/", response_model=list[PostOut])
async def read_posts(published: bool, limit: int = 5, skip: int = 1):
    posts  = await  service.read_all(published  = published, limit =  limit, skip = skip)
    return  posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn):
    
    id_post = await service.create_post(post)
    return {**post.model_dump(), "id": id_post}

@router.patch("/{id}", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def update_post(post: PostUpdate, id: int):
    return await service.update_post(post=post, id=id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_post(id: int):
    await service.delete_post(id)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=PostOut)
async def get_post(id: int):
    return await service.read(id)
