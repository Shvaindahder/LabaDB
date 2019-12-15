import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    TEMPLATE_FOLDER = os.path.join(BASEDIR, "templates")
    STATICFILES_FOLDER = os.path.join(BASEDIR, "static")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
