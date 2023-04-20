from typing import Union, Dict

import datetime

from db import db

userToJason = Dict[str, Union[int, str]]

class UserPermissionModel(db.Model):
    __tablename__ = 'userpermissions'

    user_id = db.Column(db.String(), db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
    permission = db.relationship("PermissionModel")
    granted_date = db.Column(db.TIMESTAMP(), default=datetime.datetime.now())
    
    
    def __init__(self, user_id, permission_id):
        self.user_id = user_id
        self.permission_id = permission_id

    def __repr__(self):
        return f"UserPermissionModel(user_id='{self.user_id}', permission_id='{self.permission_id}', \
                 granted_date='{str(self.granted_date)}')"
                 
    def to_json(self) -> Dict[str, Union[int, str]]:
        return {
            'user_id': self.user_id,
            'granted_date': str(self.granted_date),
            'permission': self.permission.to_json()
            
        }
        
    def insert(self) -> 'UserPermissionModel':
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            raise
        
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_userpermission_by_id(cls, user_id: str, permission_id) -> 'UserPermissionModel':
        try:
            return cls.query.filter_by(user_id=user_id, permission_id=permission_id).first()
        except:
            raise