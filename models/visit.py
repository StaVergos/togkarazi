from db import db


class TaskModel(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    date_started = db.Column(db.Date, nullable=False)
    date_finished = db.Column(db.Date, nullable=False)
    tasks = db.relationship('TaskModel', backref='task', lazy=True)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name: str) -> "VisitModel":
        return cls.query.filter_by(name=name).all()
