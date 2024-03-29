from db import messages_collection, user_collection
import json
from html import escape
from bson import ObjectId
from util.auth import get_user_data
from functions.spotify import spotifyPlaybackFunction 

# getting all chat messages
def getChatMessagesFunction():
    message_list = list(
        messages_collection.find({})
    )
    for message in message_list:
        message['id'] = message.pop('_id')
        message['id'] = str(message['id'])
    message_list = json.dumps(message_list)
    content, mime_type = message_list, 'text/plain'
    return f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: {mime_type}\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content.encode('utf-8')


# sending a chat message 
def sendChatMessagesFunction(request):
    message = json.loads(request.body.decode('utf-8'))['message']
    message = escape(message)
    payload = {}
    
    if request.cookies.get('id') == None:
        payload = {
            'username': 'Guest',
            'message': message
        }
        content = json.dumps(payload)
        messages_collection.insert_one(payload)
        return f"HTTP/1.1 201 CREATED\r\nContent-Length: {len(content)}\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content.encode('utf-8')
    else:
        user_data = get_user_data(request)
        xsrf_token_header = request.headers.get('X-XSRF-Token')
        xsrf_token_database = user_data['xsrf_token']
        if user_data:
            spotify_access_token = get_user_data(request).get('spotify_access_token')
            if spotify_access_token:
                payload = {
                        'username': user_data['username'],
                        'message': message + spotifyPlaybackFunction(spotify_access_token)
                }
            else:
                payload = {
                        'username': user_data['username'],
                        'message': message
                }
        else:
            payload = {
                'username': 'Guest',
                'message': message
            }
        content = json.dumps(payload)
        # Check XSRF Token
        if xsrf_token_header == xsrf_token_database:
            messages_collection.insert_one(payload)
            return f"HTTP/1.1 201 CREATED\r\nContent-Length: {len(content)}\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content.encode('utf-8')
        else:
            return f"HTTP/1.1 403 FORBIDDEN\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode()
    
# deleting a chat message
def deleteMessageFunction(request):
    if request.cookies.get('id'):
        username = get_user_data(request)['username']

        message_id = ObjectId(request.path.split('/')[2])
        try:
            message_username = messages_collection.find_one({'_id': message_id})['username']
            if message_username == username:
                messages_collection.delete_one({'_id': message_id})
                return f"HTTP/1.1 200 Good\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nYour message has been deleted".encode()
            else:
                return f"HTTP/1.1 403 Not your chat\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nThat is not your message, you cant delete".encode()
        except Exception as e:
            return f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nMessage ID Not Found".encode()
    else:
        return f"HTTP/1.1 403 Not your chat\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nThat is not your message, you cant delete".encode()


# displaying chat message with url
def retrieveMessageFunction(request):
    message_id = request.path.replace("/chat-messages/", "")
    try:
        message_objectid = ObjectId(message_id)
        message = messages_collection.find_one({'_id': message_objectid})
        message['id'] = str(message.pop('_id'))
        content, mime_type = json.dumps(message), 'text/plain'
        return f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: {mime_type}\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content.encode('utf-8')
    except Exception as e:
        return f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nMessage ID Not Found".encode()

# updates a message
def updateMessageFunction(request):
    path = request.path
    message_id = path.replace("/chat-messages/", "")
    try:
        body = request.body
        path = request.path
        message_id = path.replace("/chat-messages/", "")

        body_str = body.decode('utf-8')
        body_dict = json.loads(body_str)
        messages_collection.update_one({'_id': ObjectId(message_id)}, {"$set": body_dict})
        body_dict['id'] = message_id
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + json.dumps(body_dict).encode('utf-8')
    except Exception as e:
        return f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nMessage ID Not Found".encode()
