from fastapi import FastAPI
from configuration import tags_metadata

app = FastAPI(openapi_tags=tags_metadata)

