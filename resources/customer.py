from flask_restful import Resource

from models.customer import CustomerModel
from schemas.customer import CustomerSchema
from libs.strings import gettext


customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)


class Customer(Resource):
    @classmethod
    def get(cls, name: str):
        store = CustomerSchema.find_by_name(name)
        if store:
            return customer_schema.dump(store), 200
        return {"message": gettext("customer_not_found")}, 404

    @classmethod
    def post(cls, name: str):
        customer = CustomerModel(name=name)
        try:
            customer.save_to_db()
        except:
            return {"message": gettext("customer_error_inserting")}, 500

        return customer_schema.dump(customer), 201

    @classmethod
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
