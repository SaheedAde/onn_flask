import flask_restx
from functools import wraps
from bson.objectid import ObjectId
from .util import verify_auth_token
from flask import Blueprint, request
from .models import products as products_db
from flask_restx import Resource, abort, fields


app = Blueprint('admin', __name__)
admin_authorizations = {
    'admin_api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
router = flask_restx.Api(
    app,
    doc='/admin-doc/',
    authorizations=admin_authorizations,
    security='admin_api_key'
)

products = router.model('ProductList', {
    'title': fields.String(description='Name of product'),
    'description': fields.String(description='Description of product'),
    'price': fields.String(required=True, description='price'),
    'stock': fields.String(description='stock left'),
})

response = router.model('ProductListResp', {
    'code': fields.Integer(required=True, description='Status code'),
    'product_id': fields.String(required=True, description='id')
})

delete_response = router.model('ProductDeleteResp', {
    'code': fields.Integer(required=True, description='Status code'),
    'message': fields.String(required=True, description='id')
})



def admin_auth_token_required():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_admin_token = request.headers.get('X-ADMIN-AUTH')
            if auth_admin_token:
                result = verify_auth_token(auth_admin_token)
                if not result.get('is_valid'):
                    abort(403, 'Token Expired')
                resp = result['response']
                if resp.get('user_id') != 'test_admin':
                    abort(403, message='Access denied')
                print('PASSED')
                return func(*args, **kwargs)
            abort(403, message='Access denied')

        return wrapper
    return decorator

@router.route('/products', defaults={'product_id': None})
@router.route('/products/<string:product_id>')
class Products(Resource):
    @router.doc(security='admin_api_key')
    @router.expect(products, validate=True)
    @router.marshal_list_with(response)
    @admin_auth_token_required()
    def post(self, product_id):
        title = self.api.payload.get('title', '')
        price = self.api.payload.get('price', '')
        stock = self.api.payload.get('stock', '')
        description = self.api.payload.get('description', '')
        try:
            int(stock)
        except ValueError:
            abort(403, message='Quantity Must Be Number Type')

        product = products_db.insert_one({
            'title': title,
            'price': price,
            'stock': stock,
            'description': description
        })
        resp = {
            'code': 200,
            'product_id': product.inserted_id
        }
        return resp

    @router.doc(security='admin_api_key')
    @admin_auth_token_required()
    @router.marshal_list_with(delete_response)
    def delete(self, product_id):
        prod = products_db.delete_one({"_id": ObjectId(product_id)})
        if prod.deleted_count:
            return {'code': 200, 'message': 'Deletetion succesful'}
        return {'code': 200, 'message': 'No data with id in database'}
