from authentication.helper import CreateUserAuthData, UserCredentialValidation
from authentication.schema import UserNamePass
from typing import Any
from fastapi import APIRouter
router=APIRouter()


# collection.delete_many({}) 
# used to delete every data from table

"""
Below is post HTTP request used to create user details.
and store user information in database (Mongodb)

"""
@router.post("/user/signup",response_model=Any)
async def signup(user: UserNamePass): # using form also work
    check_valid=UserCredentialValidation.username_email_phone_validation(user)
    key=""
    for valid in check_valid:
        key=valid + ", "
    if len(key)!=0:
        return "Sorry! "+key+ "already exist. Try another one!"
    user_auth_information=CreateUserAuthData.create_user_authenication(user)
    if user_auth_information:
        return "you register succesfully. Your id "+ str(user_auth_information)
    return "Sorry, You registration was not successful. Try again"