# from celery import Celery
from celery import shared_task
import numpy as np
from sklearn.linear_model import LinearRegression


@shared_task
def flight_prediction():
    pass