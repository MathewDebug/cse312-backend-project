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
    parts_list = [part for part in parts_list if part.strip()]

    object_part_list = []
    for part in parts_list:
        header_dict, name = {}, b''
        if part.startswith(b'\r\n'):
            content = part.split(b'\r\n\r\n')[1:]
            content = b'\r\n\r\n'.join(content)
            if content.endswith(b'\r\n'):
                content = content[:-2]
            for h in part.split(b'\r\n\r\n')[0].split(b'\r\n')[1:]:
                header_dict[h.split(b': ')[0].decode()] = h.split(b': ')[1].decode()
                if h.startswith(b'Content-Disposition'):
                    name_idx = h.find(b'name=')
                    if name_idx != -1:
                        name = h[name_idx:].split(b'"')[1]

            object_part_list.append(Part(header_dict, name.decode(), content))
    return MultipartData(boundary, object_part_list)

# r = Request(b'POST /form-path HTTP/1.1/\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJes\r\n\r\ns\xffe\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="upload"; filename="discord.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of_the_file>\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia--')
# multipart_test1 = parse_multipart(r)
# print(multipart_test1.parts[0].headers, multipart_test1.parts[0].name, multipart_test1.parts[0].content)
# print(multipart_test1.parts[1].headers, multipart_test1.parts[1].name, multipart_test1.parts[1].content)

# r2 = Request(b'POST /form-path HTTP/1.1/\r\nContent-Length: 9937\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundarycriD3u6M0UuPR1ia\r\n\r\n------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJess\xffe')
# multipart_test2 = parse_multipart(r2)
# print(multipart_test2.boundary, multipart_test2.parts[0].headers, multipart_test2.parts[0].name, multipart_test2.parts[0].content)

#------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="commenter"\r\n\r\nJesse\r\n
#------WebKitFormBoundarycriD3u6M0UuPR1ia\r\nContent-Disposition: form-data; name="upload"; filename="discord.png"\r\nContent-Type: image/png\r\n\r\n<bytes_of_the_file>\r\n
#------WebKitFormBoundarycriD3u6M0UuPR1ia--')

