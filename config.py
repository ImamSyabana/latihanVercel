import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
    SQLALCHEMY_DATABASE_URI= os.getenv('Database_URL', 'postgresql://neondb_owner:npg_yq8e9NTzQvjr@ep-shy-wildflower-adhv56i1-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require')
    SQLALCHEMY_TRACK_MODIFICATIONS = False