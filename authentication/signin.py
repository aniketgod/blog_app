from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from authentication.helper import Authenication, timedelta, Error, CreateDeleteSession, ACCESS_TOKEN_EXPIRE_MINUTE
import json
from typing import Any 
import logging

router=APIRouter()

"""
OAuth2PasswordBearer provide framework to authenciate user by swager authorization.
"""
ouath2_scheme= OAuth2PasswordBearer(tokenUrl= "/user/signin")


"""
The below post HTTP request at /signin help to create user jwt token.
Steps Details:
1. Takes the data from user in Format of RequestForm.
2. Extract the data from form_data
3. first authenicate the user
4. If user is not successfully authenicate. Then raise HTTP exception.
5. If user is successfully authenicate. Then Create the jwt token.
6. return jwt token in format:
       {"access_token":access_token, "token_type":"bearer"}
       directly send access_token or use another key word for sending access_token 
       it will not work.
"""

@router.post("/user/signin", response_model=Any)
async def signin(form_data: OAuth2PasswordRequestForm = Depends()): 
     user_exist= Authenication.authenicate_user(form_data.username, form_data.password)
     if not user_exist: 
          raise Error.credential_error
     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
     access_token=Authenication.get_token(data={"sub":form_data.username},token_expire_time=access_token_expires)
     CreateDeleteSession.get_active_user_session(access_token)
     return {"access_token":access_token, "token_type":"bearer"}

"""

The below post HTTP request at /user/session help to check which user is sign in 
in application. It actually also confirm about jwt token is valid or not and user is logout or not
Step:
1. it read  data from json file in which token data keep in API.json
2. use try and catch method if token exist in API.json file then try
block fully run and it will execute raise HTTP exception.
otherwise if token not exist in API.json 
then it verify the jwt token is valid or not.
if everything is okay then /user/session return active user at that instance.
"""

@router.get("/user/session", response_model=Any)
async def create_session(token: str = Depends(ouath2_scheme)):
     API_token_file=open("./utilis/API.json","r")
     json_object=json.load(API_token_file)
     try: 
          json_object["token_key"].index(token)
          raise Error.credential_error()
     except ValueError:
          logging.error(ValueError)
     API_token_file.close()
     user= CreateDeleteSession.get_active_user_session(token)
     return user
  
"""
The HTPP request /user/logout  used to logout from application.
1. it read  data from json file in which token data keep in API.json
2. use try and catch method if token exist in API.json file then try
block fully run and it will execute raise HTTP exception.
otherwise if token not exist in API.json 
then it open the file API.json in writing formatte and add token.
In the end it also verify the jwt token is valid or not.
if everything is okay then /user/logout the return active user at that instance.
"""

@router.get("/user/logout", response_model=Any)
async def logout_session(token: str = Depends(ouath2_scheme)):
     API_token_file=open("./utilis/API.json","r")
     json_object=json.load(API_token_file)
     try: 
          json_object["token_key"].index(token)
          logging.error("Message: the token is already exist")
          CreateDeleteSession.get_logout_session(token)
          raise Error.credential_error()
     except ValueError:
          logging.error(ValueError)
     API_token_file.close()
     API_token_file=open("./utilis/API.json","w")
     data=json_object["token_key"]
     data.append(token)
     json_object["token_key"]=data
     json.dump(json_object, API_token_file)
     API_token_file.close()
     user= CreateDeleteSession.get_logout_session(token)
     return user