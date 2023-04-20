from flask_restful import Resource
from Security.Args import userParser
from werkzeug.security import check_password_hash, generate_password_hash  # safe_str_cmp,
import datetime
from Models.UserModel import UserModel
from Models.PermissionModel import PermissionModel

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    fresh_jwt_required,
    jwt_required,
    get_jwt_identity,  # This return Login User Identity
    get_raw_jwt,
)
from Security.blacklist import BLACKLIST


class User(Resource):
    
    # Create User
    @classmethod
    def post(cls):
        try:
            response_data = userParser.parse_args()
            response_data['email'] = response_data['email'][0]
            response_data['dateofbirth'] = response_data['dateofbirth'][0]
            if UserModel.get_user_by_email(response_data['email']):
                return {'message': 'User with the same email already exists'}, 400  # Bad Request

            # This hash the password
            response_data['password'] = generate_password_hash(response_data['password'])

            user = UserModel(None, **response_data)
            user.insert_user()
            
            return {'message': 'User created successfully'}, 201  # Created
        
        except Exception as e:
            
            return {'message': e.data}, 500  # Server Error

class Users(Resource):
            
    # Get User
    # @jwt_required
    def get(self, email: str):
        try:
            user = UserModel.get_user_by_email(email)
            if user:
                return user.to_json(), 200
            
            return {'message': 'Record not found'}, 400
        
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error

    @classmethod
    # Delete User
    def delete(cls, email: str):
        
        try:
        
            user = UserModel.get_user_by_email(email)
        
            if not user:
                return {"message": "User not found."}, 404
        
            user.delete()
        
            return {"message": "User deleted successfully."}, 200
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error
        
class AllUsers(Resource):
    def get(self):
        try:
            users = UserModel.get_all_users()
            users = [user.to_json() for user in users]
            return users
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error

class UsersByLastName(Resource):
    def get(self, lastname):
        try:
            users = UserModel.get_user_by_lastname(lastname)
            users = [user.to_json() for user in users]
            return users
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error

class UserLogin(Resource):
    @classmethod
    def post(cls):
        response_data = userParser.parse_args()
        response_data['email'] = response_data['email'][0]

        user = UserModel.get_user_by_email(response_data["email"])
        if user and check_password_hash(user.password, response_data["email"]):
            access_token = create_access_token(identity=user.id,
                                               fresh=True,
                                               expires_delta=datetime.timedelta(minutes=5))
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials!"}, 400  # Bad request

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": "User <id={}> successfully logged out.".format(user_id)}, 200

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200

