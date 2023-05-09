from . import api
from ..models import Product
from ..apiauthhelper import token_auth
from flask import request

# for full products page
@api.get('/products')
def getProductsAPI():
    products = Product.query.all()
    return {
        'status':'ok',
        'results':len(products),
        'products': [prod.to_dict() for prod in products]
    }

# for querying, this includes if the user hasn't searched for anything, so the above method should be covered here
@api.get('/productsq=<string:search_name>')
@api.get('/productsq=')
def getSearchedProductsAPI(search_name=''):
    # if the user has searched something
    if search_name.strip():
        # ilike is case insensitive
        products = Product.query.filter(Product.title.ilike("%" + search_name + "%")).all()
    else:
        products = Product.query.all()
    return {
        'status':'ok',
        'results':len(products),
        'products': [prod.to_dict() for prod in products]
    }

# for single product page
@api.get('/products/<int:product_id>')
def getProductAPI(product_id):
    product = Product.query.get(product_id)
    if product:
        return {
            'status':'ok',
            'results':1,
            'product': product.to_dict()
        }
    else:
        return {
            'status':'not ok',
            'message': 'The product you are looking for does not exist.'
        }, 404
