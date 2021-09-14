from ma import ma
from models.part import PartModel
from models.task import TaskModel


class PartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PartModel
        load_only = ("task",)
        dump_only = ("id",)
        load_instance = True
        include_fk = True
