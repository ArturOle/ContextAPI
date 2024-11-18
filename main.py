import os

app_path = "src.context_api.api:app"

os.system(f'gunicorn {app_path} -k uvicorn.workers.UvicornWorker --name context-search --bind=unix:/home/ubuntu/proj/ContextAPI/run/gunicorn.sock --log-level debug --access-logfile logs.log --keep-alive 0 --daemon')
