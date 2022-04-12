from authentication.schema import UserDetail, GetId, login_status,UserNamePass
from utilis.db_connection import user_auth_table
from utilis.constant import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import HTTPException, status
from typing import Optional
from datetime import timedelta, datetime
from jose import jwt
from passlib.context import CryptContext
from utilis.logging import logging


ACCESS_TOKEN_EXPIRE_MINUTE=int(ACCESS_TOKEN_EXPIRE_MINUTES)
"""
pwd_context actally secure our password in  hashing format
it make hash_password human to understand hard and breaking password by software is also hard
"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
class Error:
     @staticmethod
     def credential_error():
          return HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Could not validate credentials",
           headers={"WWW-Authenticate": "Bearer"},
           )

        
class Authenication:
     @staticmethod
     def get_token(data: dict, token_expire_time: Optional[timedelta]= None):
          data_for_encode= data.copy()
          if token_expire_time:
               token_expire= datetime.utcnow()+token_expire_time
          else:
               token_expire=datetime.utcnow()+timedelta(minutes=15)
          data_for_encode.update({"exp":token_expire})
          encoded_jwt=jwt.encode(data_for_encode,SECRET_KEY,algorithm=ALGORITHM)
          return encoded_jwt
     """
     get_token method used create token in jwt formatte the method used to 
     create  jwt token given below encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
     step
     1. firstly seting expiry time of jwt.
               token_expire= datetime.utcnow()+token_expire_time.
     2. then update encode detail
               to_encode.update({"exp":token_expire})
     then return jwt token
     and encode exp details in to encode variable.
     after that data in to_encode encode in jwt token and return token.
     """

     def get_verify_pass(password: str, hash_password: str ):
          return pwd_context.verify(password,hash_password)
     """
     get verify pass method simply verify the password and hash_password
     by using inbuilt verify method of crptocontext.

     """

     def authenicate_user(username: str, password: str):
          user=UserData.get_user_by_username(username)
          user_auth_data=GetId(**user)
          if user_auth_data==False:
            return False
          verify_password=Authenication.get_verify_pass(password,user_auth_data.hash_password)
          if not verify_password:
               return False
          return True
     """
     authenicate user method simply verify the user and password by using CryptoContext verify method.
     """

class CreateDeleteSession:
     @staticmethod
     def update_login_status(user: login_status, status: bool):
          user_auth_data=user_auth_table.find({"username":user.username})
          user_auth_data_list=list(user_auth_data)
          user_auth_data_list[0]["user_login_status"]=status
          user_auth_table.update({"username":user.username},dict(login_status(**user_auth_data_list[0])))
          updated_data=user_auth_table.find({"username":user.username})
          user_auth_data=list(updated_data)
          return user_auth_data
     """
     update_login_status method used to update the status if status in parameters is True then set true.
     Otherwise set login_status false. 
     """
     def get_logout_session(token: str):
          try:
               payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
               username : str = payload.get("sub")
               if username is None:
                    return Error.credential_error()
          except Exception as e:
               logging.error(e)
               return Error.credential_error()
          user_auth_data=GetId(**UserData.get_user_by_username(username))
          user_auth_data_list=CreateDeleteSession.update_login_status(user_auth_data, False)
          return UserDetail(**(user_auth_data_list[0]))
     """
     The logout_session method and user_session method is similar the only difference is that in logout session 
     the login_status is setting false. 
     """
     def get_user_session(token: str):
          try:
               payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
               username : str = payload.get("sub")
               if username is None:
                    return Error.credential_error()
          except Exception as e:
               logging.error(e)
               return Error.credential_error()
          user_auth_data=GetId(**UserData.get_user_by_username(username))
          updated_user_list=CreateDeleteSession.update_login_status(user_auth_data,True)
          updated_user=updated_user_list[0]
          return UserDetail(**updated_user)
     """
     get_user_session method used to the check validation of token and setting login status is true.
     Step: 
     1. decoding the jwt token by method 
     jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
     and store in payload mode.
     Note: algorithms in jwt.decode and algorithm in jwt.encode 
     Note: algorithm takes the value in list formate 
     The parameteres in jwt.encode and jwt.decode slightly different keep in note.
     after decode  check username is not none.
     if user is not none then
     get user_by_username method and  return the user detail in GetId model. 
     keep in mind Get_id model have a variable id but it will not take value type objectid it alawys be none.
     in the end return user the user detail by using user_detail model.
     """

     def get_active_user_session(token: str):
          user_session= CreateDeleteSession.get_user_session(token)
          return user_session

class UserData:
     @staticmethod
     def get_user_by_username(username: str):
          user_auth_data=user_auth_table.find({"username":username})
          user_auth_data_list=list(user_auth_data)
          if len(user_auth_data_list)==0:
               return False
          return dict(**user_auth_data_list[0])


class CreateUserAuthData:
    @staticmethod
    def create_user_authenication(user: UserNamePass):
        hash_password=UserCredentialValidation.get_hash_password(user.password)
        user_auth_data=dict(user)
        user_auth_data["hash_password"]=hash_password
        user_auth_data["user_login_status"]=False
        try:
            user_auth_data=user_auth_table.insert_one(user_auth_data)
        except Exception as e:
            logging.exception("Failed to insertion",e)
            return False
        return  user_auth_data.inserted_id
    """
    create_user_auth () method used to create user details.
    The method used to store user personal information in database.
    in hash_password variable, we can not directly manipulate data.
    so, we have to first make dictionary for them. 
    """
class UserCredentialValidation:
    @staticmethod
    def username_email_phone_validation(user: UserNamePass):
        crenditial_invalid=[]
        email_exist=user_auth_table.find({"email":user.email})
        if email_exist.count()!=0:
            logging.error("The user try to registration with same email : "+user.email)
            crenditial_invalid.append("Email")

        phone_no_exist=user_auth_table.find({"phone_no": user.phone_no})

        if phone_no_exist.count()!=0:
            logging.error("The user try to registration with same phone no : "+ str(user.phone_no))
            crenditial_invalid.append("Phone Number")

        username_exist=user_auth_table.find({"username": user.username})
        if username_exist.count()!=0:
            logging.error("The user try to registration with same username : "+user.username)
            crenditial_invalid.append("User Name")
        return crenditial_invalid
    """
    check_user_validation is used to validate user information actuallly.
    it help to check email, phone_no and username should be unique.
    """
    def get_hash_password(password: str):
        return pwd_context.hash(password)
    """
    get_hash_password() method used to create password in hash password.
    The method used to create hash password is 
    CryptoContext(schemes=["bcrypt"], deprecated="auto").hash(user_password)
    """