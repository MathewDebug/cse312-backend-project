import socketserver

from util.request import Request
from util.auth import get_user_id, get_user_data

from functions.chat import deleteMessageFunction, retrieveMessageFunction, getChatMessagesFunction, sendChatMessagesFunction, updateMessageFunction
from functions.auth import loginFunction, logoutFunction, registerFunction
from functions.spotify import loginSpotifyFunction, spotifyCallbackFunction
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        received_data = self.request.recv(2048)
        if not received_data.decode('utf-8').startswith('GET /chat-messages'):
            print(self.client_address)
            print("--- received data ---")
            print(received_data)
            print("--- end of data ---\n\n")

        request = Request(received_data)
        path = request.path
        method = request.method

        # Root path
        if path == '/':
            path = '/public/index.html'

        # Mime type
        if len(path.split('.')) >= 2:
            file_type = path.split('.')[1]
            mime_type = "text/plain"
            if file_type == "html" or file_type == "css":
                mime_type = "text/" + file_type
            elif file_type == "jpg" or file_type == "ico":
                mime_type = "image/" + file_type
            elif file_type == "js":
                mime_type = "text/javascript"

            file_path = path.lstrip("/")

            self.sendResponse(file_path, mime_type, request)
        elif path == "/chat-messages" and method == "GET":
            self.getChatMessages()
        elif path == "/chat-messages" and method == "POST":
            self.sendChatMessages(request)
        elif path.startswith('/chat-messages/') and method == "GET":
            self.retrieveMessage(request)
        elif path.startswith('/chat-messages/') and method == "DELETE":
            self.deleteMessage(request)
        elif path.startswith('/chat-messages/') and method == "PUT":
            self.updateMessage(request)
        elif path == '/register' and method == "POST":
            self.register(request)
        elif path == '/login' and method == "POST":
            self.login(request)
        elif path == "/logout" and method == "POST":
            self.logout(request)
        elif path == "/login-spotify" and method == "POST":
            self.loginSpotify(request)
        elif path.startswith('/spotify') and method == "GET":
            self.spotifyCallback(request)
        else:
            self.request.sendall("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nContent not found".encode())

    # CHANGE DOCKER-COMPOSE YML FILE WITH SPOTIFY, CHANGE SPOTIFY CLIENT_ID, REDIRECT_ID, CHANGE DATABASE MONGODB
            

    # Auth ------------------------------------------------------------
    def logout(self, request):
        self.request.sendall(logoutFunction(request))
    
    def register(self, request):
        self.request.sendall(registerFunction(request))

    def login(self, request): 
        self.request.sendall(loginFunction(request))

    # Spotify ------------------------------------------------------------
    def loginSpotify(self, request): 
        self.request.sendall(loginSpotifyFunction(request))

    def spotifyCallback(self, request):
        self.request.sendall(spotifyCallbackFunction(request))

    # Chat ------------------------------------------------------------
    def updateMessage(self, request):
        self.request.sendall(updateMessageFunction(request))

    def deleteMessage(self, request):
        self.request.sendall(deleteMessageFunction(request))

    def retrieveMessage(self, request):
        self.request.sendall(retrieveMessageFunction(request))

    def getChatMessages(self):
        self.request.sendall(getChatMessagesFunction())

    def sendChatMessages(self, request):
        self.request.sendall(sendChatMessagesFunction(request))
        
    # Other ------------------------------------------------------------
    def sendResponse(self, file_path, mime_type, request):
        if mime_type == 'text/html':
            # pull from databse 
            
            if request.cookies.get('visits') == None:
                visits = 1
            else:
                visits = int(request.cookies['visits']) + 1

            try:
                with open(file_path, 'rb') as file:
                    content = file.read()
                    content = content.decode().replace('{{visits}}', str(visits)).encode()
                    if get_user_id(request) != None:
                        xsrf_token = get_user_data(request)['xsrf_token']
                        content = content.decode().replace('{{xsrf_token}}', xsrf_token).encode()
                    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: {mime_type}; charset=UTF-8\r\nSet-Cookie: visits={visits}; Max-Age=3600;\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content
            except Exception:
                response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nContent not found".encode()
        elif mime_type == 'text/css' or mime_type == 'image/jpg' or mime_type == 'image/ico' or mime_type == "text/javascript":
            try:
                with open(file_path, 'rb') as file:
                    content = file.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: {mime_type}\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content
            except Exception:
                response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nContent not found".encode()
        else: 
            response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nContent not found".encode()
        self.request.sendall(response)

def main():
    host = "0.0.0.0"
    port = 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((host, port), MyTCPHandler)

    print("Listening on port " + str(port))

    server.serve_forever()


if __name__ == "__main__":
    main()
