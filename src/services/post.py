from databases.interfaces import Record
from fastapi import HTTPException, status

from database import database
from models.post import posts
from schemas.post import PostIn, PostUpdate
from views.post import PostOut


class PostService:
    async def read_all(self, published: bool, limit: int = 5, skip: int = 0) -> list[Record]:
        query = posts.select().where(posts.c.published == published).limit(limit).offset(skip)
        return await database.fetch_all(query)



    async def create_post(self, post: PostIn) -> int:
        command = posts.insert().values(
            title=post.title,
            content=post.content,
            published_at=post.published_at,
            published=post.published,
        )


        return await database.execute(command)

    async def update_post(self, post: PostUpdate, id: int) -> Record:
        total = await self.count(id)
        if not total:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        data = post.model_dump(exclude_unset=True)

        command = posts.update().where(posts.c.id == id).values(**data)
        await database.execute(command)

        return await self.__get_by_id(id)

    async def delete_post(self, id: int) -> None:
        command = posts.delete().where(posts.c.id == id)
        await database.execute(command)


    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def count(self, id: int) -> int:
        query = "select count(id) as total from posts where id == :id"
        result  = await database.fetch_one(query, {"id": id})
        return result.total

    async def __get_by_id(self, id) ->  Record:
        query = posts.select().where(posts.c.id == id)
        post = await database.fetch_one(query)

        if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found")
        return post