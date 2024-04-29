from util.auth import get_user_data


def sendResponseFunction(file_path, mime_type, request):
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
                if get_user_data(request) != None:
                    xsrf_token = get_user_data(request)['xsrf_token']
                    content = content.decode().replace('{{xsrf_token}}', xsrf_token).encode()
                
                response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: {mime_type}; charset=UTF-8\r\nSet-Cookie: visits={visits}; Max-Age=3600; Secure\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content
        except Exception:
            response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nContent not found".encode()
    elif mime_type == 'text/css' or mime_type == 'image/jpg' or mime_type == 'image/ico' or mime_type == 'image/png' or mime_type == 'image/gif' or mime_type == 'video/mp4'or mime_type == "text/javascript":
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\nContent-Type: {mime_type}\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode() + content
        except Exception:
            response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nContent not found".encode()
    else: 
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nContent not found".encode()

    return response