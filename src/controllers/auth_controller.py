import jwt
from flask import request, Response, json, jsonify
from datetime import datetime

from src.utils import getenv
from src.blueprints.auth import auth_bp
from src import bcrypt, db
from src.models.user_model import User


# route for login api/users/signin
@auth_bp.route('/signin', methods=['POST'])
def handle_login():
    try:
        data = request.json
        if 'email' and 'password' in data:
            user = User.query.filter_by(email=data['email']).first()

            if user:
                if bcrypt.check_password_hash(user.password, data['password']):
                    payload = {
                        'iat': datetime.utcnow(),
                        'user_id': str(user.id).replace('-', ''),
                        'firstname': user.firstname,
                        'lastname': user.lastname,
                        'email': user.email,
                    }
                    token = jwt.encode(payload, getenv('SECRET_KEY'), algorithm='HS256')
                    return jsonify(token=token)

                else:
                    return Response(
                        response=json.dumps({
                            'status': 'failed',
                            'message': 'User Password Mistmatched'
                        }),
                        status=401,
                        mimetype='application/json'
                    )
                    # if there is no user record
            else:
                return Response(
                    response=json.dumps({
                        'status': 'failed',
                        'message': "User Record doesn't exist, kindly register"
                    }),
                    status=401,
                    mimetype='application/json'
                )
        else:
            # if request parameters are not correct
            return Response(
                response=json.dumps({
                    'status': 'failed',
                    'message': 'User Parameters Email and Password are required'
                }),
                status=400,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
            response=json.dumps({
                'status': 'failed',
                'message': 'Error Occured',
                'error': str(e)
            }),
            status=500,
            mimetype='application/json'
        )


@auth_bp.route('/signup', methods=['POST'])
def handle_signup():
    try:
        data = request.json
        if 'firstname' in data and 'lastname' and data and 'email' and 'password' in data:
            user = User.query.filter_by(email=data['email']).first()
            if not user:
                user_obj = User(
                    firstname=data['firstname'],
                    lastname=data['lastname'],
                    email=data['email'],
                    password=bcrypt.generate_password_hash(data['password']).decode('utf-8')
                )
                db.session.add(user_obj)
                db.session.commit()

                payload = {
                    'iat': datetime.utcnow(),
                    'user_id': str(user_obj.id).replace('-', ''),
                    'firstname': user_obj.firstname,
                    'lastname': user_obj.lastname,
                    'email': user_obj.email,
                }
                token = jwt.encode(payload, getenv('SECRET_KEY'), algorithm='HS256')
                return Response(
                    response=json.dumps({
                        'status': 'success',
                        'message': 'User Sign up Successful',
                        'token': token
                    }),
                    status=201,
                    mimetype='application/json'
                )
            else:
                return Response(
                    response=json.dumps({
                        'status': 'failed',
                        'message': 'User already exists kindly use sign in'
                    }),
                    status=409,
                    mimetype='application/json'
                )
        else:
            return Response(
                response=json.dumps({
                    'status': 'failed',
                    'message': 'User Parameters Firstname, Lastname, Email and Password are required'
                }),
                status=400,
                mimetype='application/json'
            )

    except Exception as e:
        return Response(
            response=json.dumps({
                'status': 'failed',
                'message': 'Error Occured',
                'error': str(e)
            }),
            status=500,
            mimetype='application/json'
        )
