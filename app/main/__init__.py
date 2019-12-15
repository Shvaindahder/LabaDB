from flask import Blueprint

bp = Blueprint("main", __name__, template_folder="main")

from app.main import routes