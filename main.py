from fastapi import FastAPI, APIRouter
import authentication.signup as signup
import authentication.signin as signin
import blog.controler as  controler
from utilis.logging import logging
import cache.cache as cache
import uvicorn
"""
APIRouter is used to run HTTP request from different file
"""

router = APIRouter()
app= FastAPI()


app.include_router(signup.router)
app.include_router(signin.router)
app.include_router(controler.router)
# app.include_router(cache.router)

"""
include_router fastapi is used to bind router from different module.
That help to run fastapi.
"""

        
@app.get("/")
async def root():
    return {"message": "Lets Use this application"}

if __name__=="__main__":
    uvicorn.run(app,port=5000,host="0.0.0.0")
