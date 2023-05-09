from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api') # we don't need to specify template folder

from . import auth_routes, product_routes, cart_routes