from util.websockets import compute_accept, parse_ws_frame, generate_ws_frame
from util.auth import get_user_data




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
