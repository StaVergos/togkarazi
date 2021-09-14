from db import db


class CustomerModel(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(24), nullable=False)
    last_name = db.Column(db.String(24), nullable=False)
    nickname = db.Column(db.String(24))
    cars = db.relationship('CarModel', backref='customer', lazy=True)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name: str) -> "CustomerModel":
        return cls.query.filter_by(name=name).all()

    @classmethod
    def find_by_lastname(cls, lastname: str) -> "CustomerModel":
        return cls.query.filter_by(lastname=lastname).all()

    @classmethod
    def find_by_nickname(cls, nickname: str) -> "CustomerModel":
        return cls.query.filter_by(nickname=nickname).all()
