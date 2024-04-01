from db import user_collection, messages_collection
from util.multipart import parse_multipart
import os
from util.auth import get_user_data

# Sends image in chat
def imageUploadFunction(request):
    multi_request = parse_multipart(request)
    print("image upload")
    for part in multi_request.parts:
        print("content length: ", len(part.content))
        image_count = len([name for name in os.listdir('public/image') if os.path.isfile(os.path.join('public/image', name))])
        filename = f'image{image_count + 1}.jpg'

        filepath = os.path.join('public/image', filename)

        with open(filepath, 'wb') as file:
            file.write(part.content)
        
        if request.cookies.get('id') == None:
            payload = {
                'username': 'Guest',
                'message': f"<img src='/public/image/{filename}' />",
            }
            messages_collection.insert_one(payload)
        else:
            user_data = get_user_data(request)
            payload = {
                'username': user_data['username'],
                'message': f"<img src='/public/image/{filename}' />",
            }
            messages_collection.insert_one(payload)  
    return f"HTTP/1.1 302 Found\r\nLocation: /\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode()

def movieUploadFunction(request):
    print("MOVIE UPLOAD")
    return b''
