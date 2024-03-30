class Request:

    def __init__(self, request: bytes):
        if request == b'':
            self.body = b''
            self.method = ""
            self.path = ""
            self.http_version = ""
            self.headers = {}
            self.cookies = {}
        else:
            request_list = request.split(b'\r\n')

            # Method, Path, HTTP Version
            status_line = request_list[0].decode().split(' ')
            if len(status_line) < 3:
                status_line[0] = ""
                status_line[1] = ""
                status_line[2] = ""

            # Body
            body  = request.split(b'\r\n\r\n')
            if len(body) > 2:
                body = b"\r\n\r\n".join(body[1:])
            else:
                body = body[1]

            # Headers, Cookies
            header_dict = {}
            cookie_dict = {}
            header_list = request.split(b'\r\n\r\n')[0]
        
            header_list = header_list.decode().split('\r\n')
            for x in header_list[1:]:
                header = x.split(": ")
                if len(header) >= 2:
                    header_dict[header[0].lstrip()] = header[1].lstrip()
                if header[0] == "Cookie":
                    cookie_list = header[1].split(';')
                    for cookie in cookie_list:
                        c = cookie.split('=')
                        cookie_dict[c[0].lstrip()] = c[1]

            # Initialize
            self.body = body
            self.method = status_line[0]
            self.path = status_line[1]
            self.http_version = status_line[2]
            self.headers = header_dict
            self.cookies = cookie_dict


def test1():
    request = Request(b'GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "localhost:8080"  # note: The leading space in the header value must be removed
    assert request.body == b""  # There is no body for this request.
    # When parsing POST requests, the body must be in bytes, not str

    # This is the start of a simple way (ie. no external libraries) to test your code.
    # It's recommended that you complete this test and add others, including at least one
    # test using a POST request. Also, ensure that the types of all values are correct

def test2():
    request = Request(b'GET / HTTP/1.1\r\nHost: cse312.com\r\nCookie: id=1; id2=2; id3=3\r\nConnection: keep-alive\r\nAccept-Language: en-US,en\r\n\r\nhello')
    assert request.method == "GET"
    assert "Host" in request.headers
    assert request.headers["Host"] == "cse312.com"  
    assert "Cookie" in request.headers
    assert request.headers["Cookie"] == "id=1; id2=2; id3=3"
    assert "Connection" in request.headers
    assert request.headers["Connection"] == "keep-alive"
    assert request.body == b"hello"  

if __name__ == '__main__':
    test1()
    test2()
