from fastapi import FastAPI, Response
from routers.user_router import userRouter
from typing import Dict
import uvicorn

app = FastAPI()

app.include_router(userRouter)

@app.get("/")
def index() -> Dict:
    return {"hello": "world"}

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="localhost")