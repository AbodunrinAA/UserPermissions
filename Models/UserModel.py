from typing import Union, List, Dict
from sqlalchemy import func

import datetime
from uuid import uuid4

from db import db

userToJason = Dict[str, Union[int, str]]

class UserModel(db.Model):
    
    __tablename__ = "users"
    id = db.Column(db.String(), primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    dateofbirth = db.Column(db.DateTime(), default=True, nullable=False)
    timestamp = db.Column(db.TIMESTAMP(), default=datetime.datetime.now())
    permissions = db.relationship('UserPermissionModel', lazy='dynamic')


    def __init__(self, _id, firstname: str, lastname: str, email: str, password: str, dateofbirth = str):
        self.id = uuid4()
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.dateofbirth = dateofbirth

    def to_json(self) -> userToJason:
        return {'id': self.id, 'firstname': self.firstname, 'lastname': self.lastname, 'email': self.email,
                'dateofbirth': str(self.dateofbirth), 'permissions':[permission.to_json() for permission in self.permissions]}
        
    def __repr__(self):
        return f"User(id='{self.id}', lastname='{self.lastname}', firstname='{self.firstname}', \
                 birthdate='{str(self.dateofbirth)}', email='{self.email}')"

    def insert_user(self) -> 'UserModel':
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            raise

    @classmethod
    def get_user_by_email(cls, email: str) -> 'UserModel':
        try:
            return cls.query.filter_by(email=email).first()
        except:
            raise
        
    @classmethod
    def get_user_by_lastname(cls, lastname: str) -> 'UserModel':
        try:
            return cls.query.filter(func.lower(cls.lastname) == lastname.lower())
        except:
            raise

    @classmethod
    def get_user_by_id(cls, _id: str) -> 'UserModel':
        try:
            return cls.query.filter_by(id=_id).first()
        except:
            raise

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_users(cls) -> List['UserModel']:
        try:
            return cls.query.all()
        except:
            raise
