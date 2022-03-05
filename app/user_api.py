import flask_restx
from functools import wraps
from bson.objectid import ObjectId
from .util import verify_auth_token
from flask import Blueprint, request
from flask_restx import Resource, abort, fields
from .models import products as products_db, orders as orders_db


app = Blueprint('user', __name__)
user_authorizations = {
    'user_api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
router = flask_restx.Api(
    app,
    doc='/user-doc/',
    authorizations=user_authorizations,
    security='user_api_key'
)

order = router.model('Order', {
    'product_id': fields.String(description='Product ID'),
    'product_name': fields.String(description='Product Name'),
    'qty': fields.String(description='Qu<ntity'),
    'address': fields.String(description='address')
})

response = router.model('OrderResp', {
    'code': fields.Integer(required=True, description='Status code'),
    'order_id': fields.String(required=True, description='id'),
    'message': fields.String(required=True, description='id')
})


def user_auth_token_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('X-USER-AUTH')
            if token:
                result = verify_auth_token(token)
                if not result.get('is_valid'):
                    abort(403, 'Token Expired')
                resp = result['response']
                if resp.get('user_id') != 'test_user':
                    abort(403, message='Access denied')
                print('PASSED')
                return func(*args, **kwargs)
            abort(403, message='Access denied')

        return wrapper
    return decorator

@router.route('/orders')
class Orders(Resource):
    @router.doc(security='user_api_key')
    @router.expect(order, validate=True)
    @router.marshal_list_with(response)
    @user_auth_token_required()
    def post(self):
        product_id = self.api.payload.get('product_id', '')
        qty = self.api.payload.get('qty', '')
        address = self.api.payload.get('address', '')
        try:
            qty = int(qty)
        except ValueError:
            abort(403, message='Quantity Must Be Number Type')

        prod = products_db.find_one({'_id': ObjectId(product_id)})
        if not prod:
            abort(403, message='Product Does Not Exist')

        stock_rem = int(prod['stock']) - int(qty)
        if stock_rem < 0:
            abort(403, message='We dont have enough quantity')

        newvalues = { "$set": { "stock": str(stock_rem) } }
        products_db.update_one({'_id': ObjectId(product_id)}, newvalues)
        order = orders_db.insert_one({
            'product_id': product_id,
            'product_name': prod['title'],
            'quantity': str(qty),
            'address': address
        })
        resp = {
            'code': 200,
            'order_id': order.inserted_id,
            'message': 'success'
        }
        return resp

    @router.doc(security='user_api_key')
    @router.marshal_list_with(order)
    @user_auth_token_required()
    def get(self):
        # fetching all data is not a good engineering practice,
        # we can fetch in batch and create pagination
        orders = orders_db.find({})
        response = []
        for doc in list(orders):
            response.append({
                'id': doc['_id'],
                'product_id': doc['product_id'],
                'product_name': doc.get('product_name', ''),
                'qty': doc['quantity'],
                'address': doc['address']
            })

        return response
