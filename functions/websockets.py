from util.websockets import compute_accept, parse_ws_frame, generate_ws_frame
from util.auth import get_user_data
from db import user_collection, messages_collection
import json




def websocketHandshakeFunction(request):
    if (request.headers.get("Upgrade", "").lower() != "websocket" or
        request.headers.get("Connection", "").lower() != "upgrade"):
        print("Invalid WebSocket handshake: Missing required headers.")

    sec_websocket_key = request.headers.get("Sec-WebSocket-Key", "")
    accept_key = compute_accept(sec_websocket_key)

    username = "Guest"
    if get_user_data(request):    
        username = get_user_data(request)['username']
    response = f"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {accept_key}\r\n\r\n".encode()
    return response, username

def broadcastChatFunction(message, username):
    # Add to database   
    db_payload = {
        'username': username,
        'message': message
    }
    message_data = messages_collection.insert_one(db_payload)
    message_id = message_data.inserted_id 
    # Socket stuff
    socket_payload = {
        'messageType': 'chatMessage', 
        'username': username, 
        'message': message, 
        'id': str(message_id)
    }
    socket_payload = json.dumps(socket_payload)
    socket_payload = socket_payload.encode()
    return generate_ws_frame(socket_payload)

def broadcastLiveUserListFunction(websocket_connections):
    users = [user[1] for user in websocket_connections]
    socket_payload = {
        'messageType': 'updateUserList',
        'users': users
    }
    socket_payload = json.dumps(socket_payload)
    socket_payload = socket_payload.encode()    
    return generate_ws_frame(socket_payload)