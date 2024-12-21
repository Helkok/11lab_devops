from fastapi import FastAPI

from middleware.middleware import DBSessionMiddleware

app = FastAPI()
app.add_middleware(DBSessionMiddleware)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
