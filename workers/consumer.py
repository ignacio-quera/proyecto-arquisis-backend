from dotenv import load_dotenv
import os
from celery import Celery

dotenv_path = '../.env'
load_dotenv(dotenv_path)

celery_app = Celery(
    __name__,
    broker=os.environ.get('CELERY_BROKER_URL', ''),
    backend=os.environ.get('CELERY_RESULT_BACKEND', '')
)

# Configura la aplicación Celery usando el módulo de configuración
celery_app.config_from_object('celery_config.config', namespace='CELERY')
