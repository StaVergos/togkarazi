from db import db


class TaskModel(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24))
    description = db.Column(db.String)
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'), nullable=False)
    parts = db.relationship('PartModel', backref='task', lazy=True)
    price = db.Column(db.Float)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name: str) -> "TaskModel":
        return cls.query.filter_by(name=name).all()
