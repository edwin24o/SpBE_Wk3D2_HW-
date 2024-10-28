from typing import List
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import os
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

class Base(DeclarativeBase):
    pass 

db = SQLAlchemy(model_class = Base)

db.init_app(app)

# service_mechanics = db.Table(
#     'service_mechanics',
#     Base.metadata,
#     Column('ticket_id', db.ForeignKey('service_tickets.id')),
#     Column('mechanic_id', db.ForeignKey('mechanics.id'))
# )

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20),)
    car_vin: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=True)


class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(200), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20))
    address: Mapped[str] = mapped_column(db.String(100), nullable=False)
    salary: Mapped[str] = mapped_column(db.String(100), nullable=False)



class ServiceTicket(Base):
    __tablename__ = 'service_tickets'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    issue_date: Mapped[date] = mapped_column(nullable=False)
    closed_date: Mapped[date] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(db.String(20), nullable=False)
    description: Mapped[str] = mapped_column(db.String(200))
    cost: Mapped[int] = mapped_column(db.String(200)) 
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.id'))



service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    Column('ticket_id', db.ForeignKey('service_tickets.id')),
    Column('mechanic_id', db.ForeignKey('mechanics.id'))
)



if __name__ == '__main__':

        with app.app_context():
            db.create_all()

        app.run(debug=True)