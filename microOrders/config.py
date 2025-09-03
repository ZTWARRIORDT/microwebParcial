import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///orders.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONSUL_URL = os.environ.get('CONSUL_URL', 'localhost:8500')
    USERS_SERVICE = os.environ.get('USERS_SERVICE', 'users-service')
    PRODUCTS_SERVICE = os.environ.get('PRODUCTS_SERVICE', 'products-service')
