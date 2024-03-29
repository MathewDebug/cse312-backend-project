# from request import Request

def parse_multipart(r):
    class Part:
        def __init__(self, headers, name, content):
            self.headers = headers
            self.name = name
            self.content = content

    class MultipartData:
        def __init__(self, boundary, parts):
            self.boundary = boundary
            self.parts = parts

    boundary = r.headers['Content-Type'].split('boundary=')[1]
    parts_list = r.body.split(b'--' + boundary.encode())
    parts_list.pop()
    parts_list.pop(0)
    object_part_list = []
    for part in parts_list:
        header_dict, name = {}, ''

        content = part.split(b'\r\n\r\n')[1].split(b'\r\n')[0]

        for h in part.decode().split('\r\n\r\n')[0].split('\r\n')[1:]:
            header_dict[h.split(': ')[0]] = h.split(': ')[1]
            if h.startswith('Content-Disposition'):
                for h in h.split('; '):
                    if h.startswith('name='):
                        name = h.split('"')[1]
        object_part_list.append(Part(header_dict, name, content))
        print(content, header_dict, name)
    return MultipartData(boundary, object_part_list)

# r = Request(b'POST /form-path HTTP/1.1/\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="upload"; filename="discord.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of_the_file>\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia--')
# multipart_test1 = parse_multipart(r)
# print(multipart_test1.boundary)
# print("--------------")
# print(type(multipart_test1.parts[0].content))
#------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n
#------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="upload"; filename="discord.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of_the_file>\r\n
#------WebKitFormBoundarycriD3u6M0UuPR1ia--')
