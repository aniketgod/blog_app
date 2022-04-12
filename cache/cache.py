import os
from fastapi import FastAPI, Request, Response,APIRouter
from fastapi_redis_cache import FastApiRedisCache, cache
from sqlalchemy.orm import Session

LOCAL_REDIS_URL = "redis://127.0.0.1:6379"

app = FastAPI(title="FastAPI Redis Cache Example")

@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", LOCAL_REDIS_URL),
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Request, Response, Session]
    )
# WILL NOT be cached
@app.get("/data_no_cache")
def get_data():
    return {"success": True, "message": "this data is not cacheable, for... you know, reasons"}

# Will be cached for one year
@app.get("/immutable_data")
@cache(expire=30)
async def get_immutable_data():
    return {"success": True, "message": "this data can be cached indefinitely"}