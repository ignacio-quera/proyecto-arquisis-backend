from fastapi import FastAPI
from pydantic import BaseModel
from celery_config.tasks import flight_prediction # Importar la tarea de Celery

from celery.result import AsyncResult

app = FastAPI()

class Job(BaseModel):
    flightPrices: list
    recent_purchases: int
    amount: int

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/job/{job_id}')
def get_job(job_id: str):
    task = flight_prediction.AsyncResult(job_id)
    return {"ready": task.ready(), "result": task.result,}

@app.post('/job/')
def create_job(job: Job):
    task = flight_prediction.delay(job.flightPrices, job.recent_purchases, job.amount)
    return {'message': 'job published', 'job_id': task.id}

@app.get('/heartbeat')
def heartbeat():
    return {'working': 'True'}

# @app.post("/job")
# async def create_job(request: Request):
#     data = await request.json()
#     price_history = data["price_history"]
#     n = data["n"]
#     try:
#         job = predict_prices.delay(price_history, n)
#         print(f"Se agregó el job {job.id} a la cola de predicción")
#         response = {"job_id": job.id}
#         return response
#     except Exception as e:
#         print(f"Se produjo un error: {str(e)}")
#         raise HTTPException(status_code=500, detail="Error en el servidor")


# @app.get("/job/{job_id}")
# def get_job(job_id: str):
#     job = predict_prices.AsyncResult(job_id)
#     if job.ready():
#         response = {"result": job.result}
#         return response
#     else:
#         return None


# @app.get("/heartbeat")
# def heartbeat():
#     return {"status": "true"}