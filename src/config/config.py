from src.config.dev import DevConfig
from src.config.prod import ProdConfig


class Config:
    def __init__(self):
        self.dev = DevConfig()
        self.prod = ProdConfig()
