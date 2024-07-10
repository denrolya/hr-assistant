import os
from dotenv import load_dotenv


def getenv(key, default=None):
    load_dotenv()
    return os.getenv(key, default)
