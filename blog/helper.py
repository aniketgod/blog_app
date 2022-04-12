from bson import ObjectId
from blog.schema import ProperModel
from utilis.db_connection import blog_table
from authentication.helper import Error, UserData
from utilis.constant import SECRET_KEY, ALGORITHM
from jose import jwt
import logging



    
class Blog:
    @staticmethod
    def create_first_blog(blog:ProperModel, id: str):
        blog_data=dict(blog)
        blog_data["user_id"]=id
        blog_table.insert_one(blog_data)
        
    """
    create_first_blog method used to create the blog data in table of database.
    """
    def blog_delete(blog_id: str):
        id=ObjectId(blog_id)
        blog_table.delete_one({"_id":id})
    """
    blog_delete method used to delete blog by id from database

    """
    def get_all_blog(id: str):
        blog_data=blog_table.find({"user_id":id})
        blog_data=list(blog_data)
        for data in blog_data:
            for key in data:
                if (isinstance(data[key], ObjectId)):
                    data[key]=str(data[key])      
        return blog_data
    """
    get _all_blog method used to get single blog from database.
    isinstance function is check the parameter of data in blog_data is a oject id 
    if yes the change in directly in blog_data variable string.
    """
    def blog_update(blog_details: ProperModel, blog_id: str, login_status: str):
        blog_details=dict(blog_details)
        blog_details["user_id"]=ObjectId(login_status)
        blog_data={"$set":blog_details}
        blog_table.update_one({"_id":ObjectId(blog_id)},blog_data)
    
    """
    update blog method used to upodate the blog in databse
    it takes the parameter login_stautus in which user_id is kept.
    """
        
    def get_single_blog(id:str):
        blog_data=blog_table.find({"_id":ObjectId(id)})
        blog_data=list(blog_data)
        for data in blog_data:
            for key in data:
                if (isinstance(data[key], ObjectId)):
                    data[key]=str(data[key])               
        return blog_data
        
    """
    get _single_blog method used to get all blog from database.
    isinstance function is check the parameter of data in blog_data is a oject id 
    if yes the change in directly in blog_data variable string.
    """
class UserAuthenicationStatus:
    def get_login_staus(token: str):
        try:
            payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username : str = payload.get("sub")
            if username is None:
                return Error.credential_error()
        except Exception as e:
            logging.error(e)
            return Error.credential_error()
        user=UserData.get_user_by_username(username)
        if user.get("user_login_status")==False:
            return False
        return user.get("_id")
