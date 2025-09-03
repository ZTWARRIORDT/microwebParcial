import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'frontend-secret-key'
    CONSUL_URL = os.environ.get('CONSUL_URL', 'consul:8500')
