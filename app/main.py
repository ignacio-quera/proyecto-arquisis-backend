from fastapi import FastAPI
from app.db import models, database
from app.routes import router
import uvicorn

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

