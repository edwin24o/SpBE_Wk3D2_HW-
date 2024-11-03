from flask import jsonify, request
from marshmallow import ValidationError
from application.blueprints.servicetickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema, input_service_ticket_schema
from application.models import Service_ticket, db
from application.models import Mechanic, db
from datetime import datetime, timedelta
from sqlalchemy import select
from application.extension import cache, limiter

@service_tickets_bp.route('/', methods=['POST'])
@limiter.limit('2 per hour') #limiting 2 per hour
def create_service_ticket():
    try:
        service_ticket_data = input_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = Service_ticket(service_ticket_date=datetime.now(), due_date=datetime.now() + timedelta(days=7), customer_id=service_ticket_data['customer_id'])
    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201

@service_tickets_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_service_tickets():
    query = select(Service_ticket)
    service_tickets = db.session.execute(query).scalars().all()

    return service_ticket_schema.jsonify(service_tickets), 200

@service_tickets_bp.route('/<int:ticket_id>', methods=['GET'])
@cache.cached(timeout=60)
def get_service_ticket(service_ticket_id):
    service_ticket = Service_ticket.query(service_ticket_id)
    return service_ticket_schema.jsonify(service_ticket), 200


# adding mechanic
@service_tickets_bp.route('/<int:service_ticket_id>/add_mechanic/<int:mechanic_id>', methods=['POST'])
def add_mechanic(service_ticket_id, mechanic_id):
    service_ticket = Service_ticket.query(service_ticket_id)
    mechanic = Mechanic.query(mechanic_id)

   
    if mechanic in service_ticket.mechanics:
        return jsonify({"message": "Mechanic is already assigned to this ticket."}), 400
    
  
    service_ticket.mechanics.append(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200
