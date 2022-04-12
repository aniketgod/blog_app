from bson.objectid import ObjectId
from pydantic import BaseModel

"""
user detail is detail of user 
in which user have some personal 
information such as 
1. Name: first_name and last_name
2. Email: email id of user (unique)
3. Phone no: phone number of user (unique)

UserNamePass is model to store information about 
1. username of user(unique)
2. password of user 

userHashPassword: 
Password change in hash password
by using below module
from passlib.context import CryptContext

"""

class UserDetail(BaseModel):
    first_name: str
    last_name :  str
    email: str
    phone_no: int

class UserNamePass(UserDetail):
    username: str
    password: str

class UserHashPassword(UserNamePass):
    hash_password: str

class TokenData(BaseModel):
    username: str

class login_status(UserHashPassword):
    user_login_status: bool

class GetId(login_status):
    _id: ObjectId =None

"""
This file is used to create a model for Authenication of user
where as username, password, first_name and last_name :
GetId class will not work because of BaseModel doesnot support ObjectId and object id is not a iterable
"""

