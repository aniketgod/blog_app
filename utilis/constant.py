from dotenv import load_dotenv
import os


load_dotenv()

"""
load_dotenv() method is essential to run before to take data from environment file
Note: environment file should be in root
"""
MONGO_USER=os.environ.get("MONGO_USER")
MONGO_PASSWORD=os.getenv("MONGO_PASSWORD")
SECRET_KEY=os.environ.get("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


  
