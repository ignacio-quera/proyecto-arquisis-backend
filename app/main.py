"""
This module contains the FastAPI application.
"""
from fastapi import FastAPI
import uvicorn
from app.db import models, database
from app.routes import router

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)