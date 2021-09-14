from ma import ma
from models.task import TaskModel
from models.visit import VisitModel
from schemas.part import PartSchema


class TaskSchema(ma.SQLAlchemyAutoSchema):
    parts = ma.Nested(PartSchema, many=True)

    class Meta:
        model = TaskModel
        load_only = ("visit",)
        dump_only = ("id",)
        load_instance = True
        include_fk = True
