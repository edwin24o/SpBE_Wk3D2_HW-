from application.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Customer, db
from sqlalchemy import select
from application.extension import limiter



# added limit 2 per hour
@customers_bp.route("/", methods=['POST'])
@limiter.limit('2 per hour')
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

# / GET: Get all customers
@customers_bp.route("/", methods=['GET'])
def get_all_customer():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all(

    )
    return customers_schema.jsonify(customers), 200

# //<id> GET: Get customer belonging to id
@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    return customer_schema.jsonify(customer), 200

#  //<id> PUT: Update Customer
@customers_bp.route("/<int:customer_id>", methods=['PUT'])
def uodate_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer == None:
        return jsonify({"message": "invalid id"}), 400
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in customer_data.items():
        setattr(customer, field, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200

# //<id> DELETE: Delete Customer
@customers_bp.route("/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer == None:
        return jsonify({'message': "invalid id" }), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"succefuly deleted user {customer_id}!"})

