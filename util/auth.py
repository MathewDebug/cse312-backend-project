from db import user_collection, auth_tokens_collection

def extract_credentials(request):
    request_str = request.body.decode('utf-8')

    credential_split = request_str.split('&')
    username = credential_split[0].split('=')[1]

    credential_split = '&'.join(credential_split[1:]).split('=')
    password_encoded = '='.join(credential_split[1:])

    idx = 0 
    password = ''
    for a in range(len(password_encoded)):
        if idx > 0:
            idx -= 1
            continue
        
        if password_encoded[a] == '%':
            if a + 2 < len(password_encoded):
                password += chr(int(password_encoded[a+1:a+3], 16))
                idx = 2 
        else:
            password += password_encoded[a]

    return [username, password]


def validate_password(password):
    lower = False
    upper = False
    number = False
    special_char = False
    special_char_list = set('!@#$%^&()-_=')

    if len(password) < 8:
        return False
    
    for char in password:
        if char.islower():
            lower = True
        if char.isupper():
            upper = True
        if char.isdigit():
            number = True
        if char in special_char_list:
            special_char = True
        if char not in special_char_list and not char.isalnum():
            return False
    if lower == False or upper == False or number == False or special_char == False:
        return False
    return True

# Helper Functions
def get_user_data(request):
    token_hash = request.cookies['id']
    return user_collection.find_one({"auth_token": token_hash})
    
def get_user_id(request):
    token_hash = request.cookies.get('id')
    if token_hash == None:
        return None
    return user_collection.find_one({"auth_token": token_hash})['_id']
