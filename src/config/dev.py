from src.utils import getenv

class DevConfig:
    def __init__(self):
        self.ENV = "dev"
        self.DEBUG = True
        self.PORT = getenv('FLASK_RUN_PORT', '8000')
        self.HOST = '0.0.0.0'
