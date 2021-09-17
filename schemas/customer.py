from ma import ma
from models.customer import CustomerModel
from models.car import CarModel
from schemas.car import CarSchema


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    cars = ma.Nested(CarSchema, many=True)

    class Meta:
        model = CustomerModel
        dump_only = ("id",)
        load_instance = True
        include_fk = True
