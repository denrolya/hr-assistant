from src.blueprints.main import main_bp
from src.blueprints.api import api_bp
from src.blueprints.auth import auth_bp
from src.blueprints.telegram import telegram_bp


def register_blueprints(app):
    """Register all available blueprints in correct hierarchy.
    Import controllers & commands here cause otherwise flask will not be able to 'see' them"""

    # Import controllers
    import src.controllers.cover_letter_controller
    import src.controllers.auth_controller
    import src.controllers.telegram_controller

    # Import console commands
    import src.console.generate_cover_letter

    api_bp.register_blueprint(auth_bp, url_prefix="/auth")
    api_bp.register_blueprint(telegram_bp, url_prefix="/tg")
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(main_bp)
