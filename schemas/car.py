from ma import ma
from models.car import CarModel
from models.customer import CustomerModel
from schemas.visit import VisitSchema


class CarSchema(ma.SQLAlchemyAutoSchema):
    visits = ma.Nested(VisitSchema, many=True)

    class Meta:
        model = CarModel
        load_only = ("customer",)
        dump_only = ("id",)
        load_instance = True
        include_fk = True
