import os

app_path = "ContextAPI.context_api.api:api"

os.system(f'uvicorn {app_path} --reload --host=0.0.0.0 --port=8000')
