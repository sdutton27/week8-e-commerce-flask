from . import api
from ..models import Product
from ..apiauthhelper import token_auth
from flask import request

@api.get('/cart')
@token_auth.login_required # verify the token
def getCartAPI():
    # our reference to the cart table based on a user is user.products
    # I took a look at routes.py to see how we were getting the cart for the cart page in the Flask app
    # the current user (when you are using token_auth) = token_auth.current_user()
    cart = token_auth.current_user().products
    return {
        'status':'ok',
        'results':len(cart),
        'products_in_cart': [prod.to_dict() for prod in cart]
    }

@api.post('/add-to-cart/<int:product_id>')
@token_auth.login_required 
def addToCartAPI(product_id):
    #product = token_auth.current_user().product.query.get(product_id)
    product = Product.query.get(product_id)
    if product: # if the product exists
        if product in token_auth.current_user().products: # if the product is already in the cart
            return {
                'status':'not ok',
                'message':'This product is already in your cart.'
            }
        else: # product exists and is not yet in cart
            # add product to cart
            # from Routes.py
            token_auth.current_user().add_to_cart(product)
            return {
                'status': 'ok',
                'message': 'Successfully added the item to your cart.',
                'product': product.to_dict(),
                'products_in_cart':[prod.to_dict() for prod in token_auth.current_user().products]
            }

    else: # if the product does not exist in the DB
        return {
            'status':'not ok',
            'message':'This product does not exist'
        }

@api.delete('/remove-from-cart/<int:product_id>')
@token_auth.login_required
def removeFromCartAPI(product_id):
    product = Product.query.get(product_id)
    if product:
        if product in token_auth.current_user().products:
            token_auth.current_user().remove_from_cart(product)
            return {
                'status':'ok',
                'message':'Successfully removed item from cart.',
                'product_removed': product.to_dict(),
                'products_in_cart':[prod.to_dict() for prod in token_auth.current_user().products]
            }
        else:
           return {
                'status':'not ok',
                'message':'This product was not in your cart, so cannot be removed from your cart.'
            } 
    else:
        return {
            'status':'not ok',
            'message':'This product does not exist'
        }
    
@api.delete('/empty-cart')
@token_auth.login_required
def emptyCartAPI():
    if token_auth.current_user().products:
        # if there was something in the cart
        token_auth.current_user().empty_cart()
        return {
                'status':'ok',
                'message':'Successfully emptied cart.'
            }
    else:
        return {
            'status':'not ok',
            'message':'The cart was already empty.'
        }

@api.get('/item-in-cart/<int:product_id>')
@token_auth.login_required
def isItemInCartAPI(product_id):
    if token_auth.current_user().products:
        product = Product.query.get(product_id)
        if product:
            if product in token_auth.current_user().products:
                return {
                    'status':'ok', 
                    'in_cart':'true',
                    'message':'The item is in the cart.'
                    }
            else:
                return {
                    'status':'ok', 
                    'in_cart':'false',
                    'message':'The item is not in the cart.'
                    }
        else:
            return {
            'status':'not ok',
            'message':'The product you are looking for does not exist'
        }
    else:
        return {
            'status':'ok', # this is ok because it is a valid check
            'in_cart':'false',
            'message':'The cart is empty, so there are no products in it.'
        }