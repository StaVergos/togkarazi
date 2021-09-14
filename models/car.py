from db import db


class CarModel(db.Model):
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(24), nullable=False)
    model = db.Column(db.String(24), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    plate_number = db.Column(db.String, nullable=False)
    visits = db.Relationship('VisitModel', backref='visit', lazy=True)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name: str) -> "UserModel":
        return cls.query.filter_by(name=name).all()
