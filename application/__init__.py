from flask import Flask
from application.models import db
from application.extension import ma, limiter, cache
from application.blueprints.customers import customers_bp
from application.blueprints.servicetickets import service_tickets_bp
from application.blueprints.mechanics import mechanics_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = "/static/swagger.yaml"

swagger_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={"app_name": "Mechanic API"})

def create_app(config_name):
    
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

    return app
