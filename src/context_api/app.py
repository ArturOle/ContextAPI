import os


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from context_search import ContextSearch


class ContextAPI:
    def __init__(self):
        self.context_search = ContextSearch()
        self.api = FastAPI()
        self.cwd = os.getcwd()

        self.api.add_api_route("/", self.read_root)
        self.api.add_api_route(
            "/files/upload/", self.upload_file, methods=["POST"]
        )
        self.api.add_api_route(
            "/search/", self.search_context, methods=["GET"]
        )

    async def read_root(self):
        return RedirectResponse(url="/docs")

    async def upload_file(self, file: UploadFile = File(...)):
        try:
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

        return {"message": f"Successfully uploaded {file.filename}"}

    async def search_context(self, query: str):
        return self.context_search.retrive(query, 5)
