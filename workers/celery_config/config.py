
accept_content = ['application/json']
CELERY_SERIALIZER = 'json'
result_serializer = 'json'

# Importar tareas
CELERY_IMPORTS = ('celery_config.tasks', )
