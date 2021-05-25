from os import environ

from dotenv import load_dotenv

load_dotenv('local/.env/host')
environ['POSTGRES_HOST'] = 'localhost'
environ['THINGSBOARD_HOST'] = 'localhost'
environ['USERSERVICE_HOST'] = 'localhost'
