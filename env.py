import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
USERS_DATABASE_URL = os.getenv("USERS_DATABASE_URL")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_JWT_KEY = os.getenv("SECRET_JWT_KEY")
ALGORITHM = os.getenv("ALGORITHM")