import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///klymates.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '38d3327a894343a587d160644251610')
    WEATHER_API_BASE_URL = 'http://api.weatherapi.com/v1'
