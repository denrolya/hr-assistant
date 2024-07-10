from src.utils import getenv

class ProdConfig:
    def __init__(self):
        self.ENV = "prod"
        self.DEBUG = False
        self.PORT = getenv('FLASK_RUN_PORT', '8000')
        self.HOST = '0.0.0.0'
