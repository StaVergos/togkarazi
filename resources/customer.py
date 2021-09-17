from flask import request
from flask_restful import Resource

from flask_jwt_extended import jwt_required

from models.customer import CustomerModel
from schemas.customer import CustomerSchema
from libs.strings import gettext


customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)


class Customer(Resource):
    @classmethod
    @jwt_required()
    def get(cls, name: str):
        customer = CustomerSchema.find_by_name(name)
        if customer:
            return customer_schema.dump(customer), 200
        return {"message": gettext("customer_not_found")}, 404

    @classmethod
    @jwt_required()
    def post(cls, name: str):
        customer_json = request.get_json()
        customer = customer_schema.load(customer_json)
        try:
            customer.save_to_db()
        except:
            return {"message": gettext("customer_error_inserting")}, 500

        return customer_schema.dump(customer), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        customer = CustomerModel.find_by_name(name)
        if customer:
            customer.delete_from_db()
            return {"message": gettext("customer_deleted")}, 200

        return {"message": gettext("customer_not_found")}, 404


class CustomerList(Resource):
    @classmethod
    def get(cls):
        return {"stores": customer_list_schema.dump(CustomerModel.find_all())}, 200
