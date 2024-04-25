"""
This module contains the FastAPI application.
"""
from fastapi import FastAPI
<<<<<<< HEAD
<<<<<<< HEAD
from fastapi.middleware.cors import CORSMiddleware
=======
>>>>>>> 0670513 (CI fixe)
=======
from fastapi.middleware.cors import CORSMiddleware
>>>>>>> 61e2def (deploy ready)
import uvicorn
from app.db import models, database
from app.routes import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL and port
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
<<<<<<< HEAD
=======

if __name__ == "__main__":
<<<<<<< HEAD
    uvicorn.run(app, host="0.0.0.0", port=8000)
>>>>>>> 0670513 (CI fixe)

if __name__ == "__main__":
=======
>>>>>>> 4350cf0 (CI dependencies installation)
    uvicorn.run(app, host="0.0.0.0", port=8000)