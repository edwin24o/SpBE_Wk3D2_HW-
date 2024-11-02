from typing import List
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from sqlalchemy import Column, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import os
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

class Base(DeclarativeBase):
    pass 

db = SQLAlchemy(model_class = Base)
ma = Marshmallow()

db.init_app(app)
ma.init_app(app)

service_mechanics = db.Table(
    "service_mechanics",
    Base.metadata,
    Column("ticket_id", db.ForeignKey("service_tickets.id")),
    Column("mechanic_id", db.ForeignKey("mechanics.id"))
)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20))

class Service_ticket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False, unique=True)
    service_date: Mapped[date] = mapped_column(nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(1500), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False )
    salary: Mapped[float] = mapped_column(db.Float(7), nullable=False)


# ================== Schemas =====================

class CustomerSchema(ma.Schema):
    class Meta:
        model = Customer

class ServiceticketSchema(ma.Schema):
    class Meta:
        model = Service_ticket

class MechanicSchema(ma.Schema):
    class Meta:
        model = Mechanic

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

serviceticket_schema = ServiceticketSchema()
servicetickets_schema = ServiceticketSchema(many=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# =================== Routes ===================

# /customers POST: Create Customer
@app.route("/customers", methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201

# /customers GET: Get all customers
@app.route("/customers", methods=['GET'])
def create_customer():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customer_schema.jsonify(customers), 200

# /customers/<id> GET: Get customer belonging to id
@app.route("/customers/<int:id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    return customer_schema.jsonify(customer), 200

#  /customers/<id> PUT: Update Customer
@app.route("/customers/<int:id>", methods=['PUT'])
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

# /customers/<id> DELETE: Delete Customer
@app.route("/customers/<int:id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer == None:
        return jsonify({'message': "invalid id" }), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"succefuly deleted user {customer_id}!"})


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)