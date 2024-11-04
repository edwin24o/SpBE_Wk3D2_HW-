from application.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema, login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from application.models import Customer, db
from sqlalchemy import select
from application.extension import limiter
from application.utils.util import encode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash


# login customers
@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        creds = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == creds['email'])
    customer = db.session.execute(query).scalars().first()

    if customer and check_password_hash(customer.password, creds['email']):

        token = encode_token(customer.id)

        response = {
            "message": 'successfully logged in',
            "status": "success",
            "token": token
        }

    return jsonify(response), 200


@customers_bp.route("/", methods=['POST'])
@limiter.limit('2 per hour')
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    # added password to new customer data and generate pw hash
    pwhash = generate_password_hash(customer_data['password'])
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], password=pwhash)
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201


@customers_bp.route("/", methods=['GET'])
def get_all_customer():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all(

    )
    return customers_schema.jsonify(customers), 200


@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    return customer_schema.jsonify(customer), 200


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

# added token required access
@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(token_user):

    
    customer = db.session.get(Customer, token_user)

    if customer == None:
        return jsonify({'message': "invalid id" }), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"succefuly deleted user {token_user}!"})

