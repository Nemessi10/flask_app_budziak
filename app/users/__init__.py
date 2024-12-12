from flask import Blueprint

user_bp = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")
auth_bp = Blueprint("auth", __name__)

from app.users import view