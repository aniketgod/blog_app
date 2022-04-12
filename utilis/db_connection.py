from pymongo import MongoClient
from utilis.constant import MONGO_USER, MONGO_PASSWORD

MONGO_USERNAME=MONGO_USER
MONGO_PASS=MONGO_PASSWORD

"""
MongoClient method used to bind the server of mongodb cluster.
"""
cluster= MongoClient("mongodb://root:example@mongo:27017/")

db = cluster["blogapp"]
user_auth_table= db["auth"]
blog_table=db["blog"]