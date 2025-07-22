
from fastapi import FastAPI

from controllers import auth, post

app = FastAPI()
# Conectar/desconectar ao banco


app.include_router(post.router)
app.include_router(auth.router)
