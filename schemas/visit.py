from ma import ma
from models.visit import VisitModel
from models.car import CarModel
from schemas.task import TaskSchema


class VisitSchema(ma.SQLAlchemyAutoSchema):
    tasks = ma.Nested(TaskSchema, many=True)

    class Meta:
        model = VisitModel
        load_only = ("car",)
        dump_only = ("id",)
        load_instance = True
        include_fk = True
