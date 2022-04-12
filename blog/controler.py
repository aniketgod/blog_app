from re import I
from authentication.helper import Error
from blog.helper import UserAuthenicationStatus, Blog
from blog.schema import ProperModel
from fastapi import Depends, APIRouter,Header
from authentication.signin import ouath2_scheme
from typing import Optional

router=APIRouter()

""" 

get blog method used the get al blog details or blog details by id.
First check the user is login or not.
if not login then raise HTTP exception

"""
@router.get("/blogs")
async def all_blog(blog_id:str=None, token: str = Depends(ouath2_scheme)):
    blog_data=None
    loginstatus=UserAuthenicationStatus.get_login_staus(token)
    if loginstatus is False:
        raise Error.credential_error()
    if blog_id:
        blog_data=Blog.get_single_blog(blog_id)
    else:
        blog_data: list=Blog.get_all_blog(loginstatus)
    return blog_data

"""
below post method used to create a blog for user.
First check the user is login or not.
if not login then raise HTTP exception
if login then send the blog parameters in create_first_blog. it will add the new blog in database                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
"""
@router.post("/blogs")
async def write_blog(blog:ProperModel, token: str = Depends(ouath2_scheme)):
    loginstatus=UserAuthenicationStatus.get_login_staus(token)
    if loginstatus is False:
        raise Error.credential_error()
    Blog.create_first_blog(blog, loginstatus)   
    return "you successfully enter your data"

"""
Below HTTP request is used to update the blog data which are written by user.
First check the user is login or not.
if not login then raise HTTP exception
if yes login then do following instruction
1. send the parameters,
blog_id, login_status, blog_details in blog_update method that return the message 
if blog is succesfully upodated or not.
"""    
@router.put("/blogs")
async def update_blog(blog_details: ProperModel, blog_id: str, token: str = Depends(ouath2_scheme)):
    loginstatus=UserAuthenicationStatus.get_login_staus(token)
    if loginstatus is False:
        raise Error.credential_error()
    Blog.blog_update(blog_details, blog_id, loginstatus)
    return "your detail successfully update"
"""
Delete method used to delete blog data  first verify the login status of user 
if user is not login then raise HTTP Exception
if user is login then do following instruction
send parameter blog_id in blog_delete. blog_delete method used to delete blog of specific id.
after that collect the all blog of user and return to user
"""
@router.delete("/blogs")
async def delete_blog(blog_id:str, token: str=Depends(ouath2_scheme)):
    loginstatus=UserAuthenicationStatus.get_login_staus(token)
    if loginstatus is False:
        raise Error.credential_error()
    Blog.blog_delete(blog_id)
    blog_data: list=Blog.get_all_blog(loginstatus)
    return blog_data

