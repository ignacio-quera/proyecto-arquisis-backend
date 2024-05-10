from fastapi import FastAPI
from pydantic import BaseModel
from celery_config.tasks import stock_prediction # Importar la tarea de Celery

from celery.result import AsyncResult

app = FastAPI()

class Job(BaseModel):
    stockPrices: list
    recent_purchases: int
    amount: int

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/job/{job_id}')
def get_job(job_id: str):
    task = stock_prediction.AsyncResult(job_id)
    return {"ready": task.ready(), "result": task.result,}

@app.post('/job/')
def create_job(job: Job):
    task = stock_prediction.delay(job.stockPrices, job.recent_purchases, job.amount)
    return {'message': 'job published', 'job_id': task.id}

@app.get('/heartbeat')
def heartbeat():
    return {'working': 'True'}