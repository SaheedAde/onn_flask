
from pymongo import MongoClient
# client = MongoClient("mongodb://localhost:27017/")
client = MongoClient(
    host='test_mongodb',
    port=27017
)
# database
db = client["app_database"]
# collection
products = db["products"]
orders = db["orders"]