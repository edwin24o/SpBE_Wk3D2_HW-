from flask import Blueprint

service_tickets_bp = Blueprint('service_tickets_bp', __name__)

# Import routes after the blueprint is defined
from . import routes
