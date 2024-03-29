import bcrypt
from util.auth import extract_credentials, validate_password, get_user_id
from db import user_collection, auth_tokens_collection
import secrets
import hashlib
from bson import ObjectId
import os

# Logout
def logoutFunction(request): 
    user_collection.update_one(
        {"_id": get_user_id(request)}, 
        {"$set": {"xsrf_token": '', "auth_token": ''}}  
    )
    auth_tokens_collection.delete_one({'auth_token': request.cookies['id']})    
    return f"HTTP/1.1 302 Found\r\nLocation: /\r\nSet-Cookie: id=; expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode()


# Register
def registerFunction(request):
    credentials = extract_credentials(request)
    username, password = credentials[0], credentials[1]
    content = ''
    if validate_password(password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        if not user_collection.find_one({"username": username}):
            content = "Register Successful"
            user_collection.insert_one({"username": username, "password": hashed_password, "xsrf_token": '', "auth_token": ''})
        else:
            content = "Username taken"
    else:
        content = "Invalid password"
    return f"HTTP/1.1 302 Found\r\nLocation: /\r\nContent-Length: {len(content)}\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nregister".encode() + content.encode('utf-8')


# Login
def loginFunction(request): 
    credentials = extract_credentials(request)
    username, password = credentials[0], credentials[1]
    content = ''
    if validate_password(password):
        user_data = user_collection.find_one({"username": username})
        if user_data:
            hashed_password = user_data['password']
            user_id = str(user_data['_id'])
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                content = "Authentication successful!"
                # Auth Token
                token = secrets.token_hex(16)
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                # XSRF Token
                new_xsrf_token = secrets.token_hex(16)
                user_collection.update_one(
                    {"username": username}, 
                    {"$set": {"xsrf_token": new_xsrf_token, "auth_token": token_hash}}  
                )
                return f"HTTP/1.1 302 Found\r\nLocation: /\r\nSet-Cookie: id={token_hash};  Max-Age=3600; HttpOnly\r\nContent-Length: {len(content)}\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content.encode('utf-8')
            else:
                content = "Wrong password"
        else:
            content = "Wrong username"
    else:
        content = "Invalid password"
    return f"HTTP/1.1 302 Found\r\nLocation: /\r\nContent-Length: {len(content)}\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content.encode('utf-8')
