import re

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, method, path, function):
        path_regex = re.compile("^" + path)
        self.routes.append({"method": method, "path": path_regex, "function": function})
        
    def route_request(self, request):
        method, path = request.method, request.path

        for route in self.routes:
            if route['method'] == method and route['path'].match(path):
                function = route['function']
                return function(request)

        return b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nNo Path Found"