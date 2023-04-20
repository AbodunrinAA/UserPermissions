from typing import Union, Dict

from db import db

userToJason = Dict[str, Union[int, str]]

class PermissionModel(db.Model):
    __tablename__ = 'permissions'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64), nullable=False)
    user_permissions = db.relationship('UserPermissionModel', lazy='dynamic')

    def __init__(self, id, type: str):
        self.id = id
        self.type = type

    def __repr__(self):
        return f"Permission(id='{self.id}', type='{self.type}')"

    def to_json(self) -> Dict[str, Union[int, str]]:
        return {
            'id': self.id,
            'type': self.type
        }