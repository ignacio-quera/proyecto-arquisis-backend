"""
This module contains the FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.db import models, database
from app.router import router

app = FastAPI()

origins = [
    "*",  # Allow all
]   

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Replace with your frontend URL and port
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)