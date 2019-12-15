from flask import Flask
from config import Config


def create_app(config=Config):
    app = Flask(__name__, template_folder=config.TEMPLATE_FOLDER, static_folder=config.STATICFILES_FOLDER)
    app.config.from_object(config)

    from app.auth import bp as auth_bp
    from app.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app