import flask_restx
from flask import Blueprint
from .models import products as products_db
from flask_restx import Resource, fields, reqparse


app = Blueprint('public', __name__)
router = flask_restx.Api(app)


products_args = reqparse.RequestParser()
products_args.add_argument(
    'title',
    type=str,
    default='',
    help='Search by product title'
)
products_args.add_argument(
    'description',
    type=str,
    default='',
    help='Search by product description'
)

products = router.model('ProductList', {
    'id': fields.String(required=True, description='product id'),
    'title': fields.String(description='Name of product'),
    'description': fields.String(description='Description of product'),
    'price': fields.String(required=True, description='price'),
    'stock': fields.String(description='stock left'),
})


@router.route('/products')
class Products(Resource):
    @router.expect(products_args, validate=True)
    @router.marshal_list_with(products)
    def get(self):
        # fetching all data is not a good engineering practice,
        # we can fetch in batch and create pagination
        args = products_args.parse_args()
        title = args.get('title')
        desc = args.get('description')
        response = []
        if title:
            products = products_db.find({'title': title})
        elif desc:
            products = products_db.find({'description': desc})
        else:
            products = products_db.find({})
        for doc in list(products):
            response.append({
                'id': doc['_id'],
                'title': doc['title'],
                'description': doc['description'],
                'price': doc['price'],
                'stock': doc['stock']
            })
        return response
