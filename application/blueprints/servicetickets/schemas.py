from application.extension import ma
from application.models import Service_ticket
from marshmallow import fields

class ServiceSchema(ma.Schema):
    id = fields.Integer(required=False)
    customer_id = fields.Integer(required=True)
    service_ticket_date = fields.Date(required=True)
    due_date = fields.Date(required=True)


    class Meta:
        fields = ('customer_id', 'service_ticket_date', 'due_date', 'id')

service_ticket_schema = ServiceSchema()
input_service_ticket_schema = ServiceSchema(exclude=['service_ticket_date', 'due_date'])
service_tickets_schema = ServiceSchema(many=True)
