import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_injector import FlaskInjector
from injector import singleton, Binder
from flask_bcrypt import Bcrypt  # for password hashing
from flask_cors import CORS

from src.config.config import Config
from src.blueprints import register_blueprints
from src.services.groq_manager import GroqManager
from src.services.job_application_service import JobApplicationService
from src.services.printer import Printer
from src.utils import getenv

app = Flask(__name__, template_folder='views')

# Logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
app.logger.info('Starting the application')

# making our application to use dev env
config = Config().dev
app.env = config.ENV
app.secret_key = getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = getenv("SQLALCHEMY_DATABASE_URI_DEV")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.models.user_model import User


# DI Section
def configure(binder: Binder) -> None:
    binder.bind(GroqManager, to=GroqManager, scope=singleton)
    binder.bind(Printer, to=Printer, scope=singleton)
    binder.bind(JobApplicationService, to=JobApplicationService, scope=singleton)


register_blueprints(app)

FlaskInjector(app=app, modules=[configure])

CORS(app)
