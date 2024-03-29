import pymongo

# CHANGE ME
client = pymongo.MongoClient("mongodb://mongo:27017/")


# client = pymongo.MongoClient(
#     "mongodb+srv://{username}:{password}@cluster0.enonn2u.mongodb.net/?retryWrites=true&w=majority".format(
#         username='user123', password='123'
#     ),
# )

chat_db = client["chat"]
messages_collection = chat_db["messages"]

users_db = client["users"]
user_collection = users_db["user"]
auth_tokens_collection = users_db["auth_tokens"]