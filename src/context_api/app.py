import os

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from context_search import ContextSearch
origins = [
    "http://localhost",
    "https://localhost"]


class ContextAPI:
    def __init__(self):
        self.context_search = ContextSearch()
        self.api = FastAPI()
        self.cwd = os.getcwd()

        self.api.state.limiter = Limiter(
            key_func=get_remote_address,
            default_limits=["6/minute"]
        )
        self.api.add_exception_handler(
            RateLimitExceeded,
            _rate_limit_exceeded_handler
        )
        self.api.add_middleware(SlowAPIMiddleware)
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.api.add_api_route("/v1/pulse", self.read_root)
        self.api.add_api_route(
            "/files/upload/", self.upload_file, methods=["POST"]
        )
        self.api.add_api_route(
            "/search/", self.search_context, methods=["GET"]
        )

    async def read_root(self):
        return 200

    async def upload_file(self, file: UploadFile = File(...)):
        try:
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)

            self.context_search.submit([file.filename])
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

        return {"message": f"Successfully uploaded {file.filename}"}

    async def search_context(self, query: str):
        return self.context_search.retrive(query, 5)
