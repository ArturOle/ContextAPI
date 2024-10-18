import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from ragger.context_search import ContextSearch


# context_search = ContextSearch()
api = FastAPI()

cwd = os.getcwd()


@api.get("/")
async def read_root():
    return RedirectResponse(url="/docs")


@api.post("/files/upload/")
def upload_file(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
