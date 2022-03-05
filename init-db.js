db = db.getSiblingDB("app_database");
db.products.drop();
db.orders.drop();

db.products.insertMany([{
    'title': 'title',
    'price': 'price',
    'stock': 'stock',
    'description': 'description'
}]);

db.orders.insertMany([{
    'product_id': 'product_id',
    'product_name': 'title',
    'quantity': '5',
    'address': 'address'
}]);