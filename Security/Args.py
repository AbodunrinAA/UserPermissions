import datetime

from flask_restful import inputs, reqparse

# User Parser
userParser = reqparse.RequestParser()
userParser.add_argument('email',
                        type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"),
                        action='append',
                        required=True,
                        help='Username should be a valid Email Address'
                        )
userParser.add_argument('password',
                        type=str,
                        required=True,
                        help='Password is required'
                        )
userParser.add_argument('firstname',
                        type=str,
                        required=False
                        )
userParser.add_argument('lastname',
                        type=str,
                        required=False
                        )
userParser.add_argument('dateofbirth',
                        type=inputs.regex(r"(\b\d\d-[01]?\d-\d\d\d\d\b)"),
                        action='append',
                        required=True,
                        help='DateOfBirth is not a valid MM-DD-YYYY.'
                        )

userPermissionParser  = reqparse.RequestParser()

userPermissionParser.add_argument('user_id',
                        type=str,
                        required=False
                        )
userPermissionParser.add_argument('permission_id',
                        type=int,
                        required=False
                        )