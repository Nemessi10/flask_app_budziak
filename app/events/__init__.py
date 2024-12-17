from flask import Blueprint

events_bp = Blueprint('events', __name__, template_folder='templates')

from app.events import view