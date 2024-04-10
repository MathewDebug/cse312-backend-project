from db import user_collection, messages_collection
from util.multipart import parse_multipart
import os
from util.auth import get_user_data

# Sends image in chat
def fileUploadFunction(request):
    multi_request = parse_multipart(request)
    for part in multi_request.parts: 
        # MP4
        if part.content.startswith(b'\x00\x00\x00\x18\x66\x74\x79\x70') or part.content.startswith(b'\x00\x00\x00\x20\x66\x74\x79\x70'):
            image_count = len([name for name in os.listdir('public/image') if os.path.isfile(os.path.join('public/image', name))])
            filename = f'image{image_count + 1}.mp4'

            filepath = os.path.join('public/image', filename)


            with open(filepath, 'wb') as file:
                file.write(part.content)
            
            print(f"/public/image/{filename}")
            if request.cookies.get('id') == None:
                payload = {
                    'username': 'Guest',
                    'message': f'<video controls><source src="/public/image/{filename}" type="video/mp4"></video>',
                }
                messages_collection.insert_one(payload)
            else:
                user_data = get_user_data(request)
                payload = {
                    'username': user_data['username'],
                    'message': f"<video controls><source src='/public/image/{filename}' type='video/mp4'></video>",
                }
                messages_collection.insert_one(payload)  
        # JPG
        if part.content.startswith(b'\xFF\xD8\xFF'): 
            image_count = len([name for name in os.listdir('public/image') if os.path.isfile(os.path.join('public/image', name))])
            filename = f'image{image_count + 1}.jpg'

            filepath = os.path.join('public/image', filename)

            with open(filepath, 'wb') as file:
                file.write(part.content)
            print(f"/public/image/{filename}")
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
        # GIF
        if part.content.startswith(b'\x47\x49\x46\x38\x37\x61') or part.content.startswith(b'\x47\x49\x46\x38\x39\x61'): 
            image_count = len([name for name in os.listdir('public/image') if os.path.isfile(os.path.join('public/image', name))])
            filename = f'image{image_count + 1}.gif'

            filepath = os.path.join('public/image', filename)

            with open(filepath, 'wb') as file:
                file.write(part.content)
            print(f"/public/image/{filename}")
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
        # PNG
        if part.content.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'): 
            image_count = len([name for name in os.listdir('public/image') if os.path.isfile(os.path.join('public/image', name))])
            filename = f'image{image_count + 1}.png'

            filepath = os.path.join('public/image', filename)

            with open(filepath, 'wb') as file:
                file.write(part.content)
            print(f"/public/image/{filename}")
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