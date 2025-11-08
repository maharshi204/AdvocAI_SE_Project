# Alternative MongoDB Configuration using PyMongo directly
# This avoids djongo compatibility issues

from pymongo import MongoClient

# MongoDB Connection
MONGO_CLIENT = MongoClient('mongodb://localhost:27017/')
MONGO_DB = MONGO_CLIENT['advocai_db']

# Collections
USERS_COLLECTION = MONGO_DB['users']

# You can use this in your views to interact with MongoDB directly
# Example:
# from django.conf import settings
# users = settings.USERS_COLLECTION.find()