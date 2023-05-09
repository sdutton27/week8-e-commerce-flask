from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import check_password_hash
from .models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            return user
    
# We don't need this yet since we are just dealing with logging in
@token_auth.verify_token
def verify_token(token):
    user = User.query.filter_by(apitoken=token).first()
    if user:
        return user # return the valid user