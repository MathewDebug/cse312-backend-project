import pymongo

# CHANGE ME
client = pymongo.MongoClient("mongodb://mongo:27017/")

chat_db = client["chat"]
messages_collection = chat_db["messages"]

users_db = client["users"]
user_collection = users_db["user"]
auth_tokens_collection = users_db["auth_tokens"]