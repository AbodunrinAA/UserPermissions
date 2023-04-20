from flask_restful import Resource
from flask_jwt_extended import (
                jwt_required,
                fresh_jwt_required
                )

from Security.Args import userPermissionParser

from Models.UserPermissionModel import UserPermissionModel as UserPermissionModels

# Note: Sparse is better than dense


class GrantUserPermission(Resource):

    # @fresh_jwt_required
    def post(self):
        """
        :param:
        :return:
        """
        try:
            response_data = userPermissionParser.parse_args()
            if UserPermissionModels.get_userpermission_by_id(response_data['user_id'], response_data['permission_id']):
                return {'message': 'Permission already assigned to user'}, 400  # Bad request

    
            new_resource = UserPermissionModels(**response_data).insert()
        
            if new_resource:
                return {'message': 'Permission assigned successfully'}, 201  # Created
            return {'message': 'Permission not assigned successfully'}, 500  # Server Error
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error


class RevokeUserPermission(Resource):

    # @fresh_jwt_required
    def delete(self):
        try:
            response_data = userPermissionParser.parse_args()
            userPermission = UserPermissionModels.get_userpermission_by_id(**response_data)
            if userPermission:
                userPermission.delete()
                return {'message': 'Permission removed successfully'}, 200
            return {'message': 'Permission not initially assigned'}, 400
        except Exception as e:
            return {'message': str(e)}, 500  # Server Error