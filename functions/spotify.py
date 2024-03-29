import os 
import secrets
import base64
import requests
import hashlib

from db import user_collection, auth_tokens_collection
from bson import ObjectId


def loginSpotifyFunction(request):
    scope = "user-read-private user-read-email user-read-currently-playing user-read-playback-state"
    # CHANGE ME
    client_id = os.environ.get("SPOTIFY_CLIENT_ID") 
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI") 

    state = secrets.token_hex(16)
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&state={state}"
    return f"HTTP/1.1 302 Found\r\nLocation: {auth_url}\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode()



def spotifyCallbackFunction(request):
    code = request.path[14:request.path.find("&state=")]
    
    # CHANGE ME 
    client_id = os.environ.get("SPOTIFY_CLIENT_ID") 
    redirect_uri = os.environ.get("SPOTIFY_REDIRECT_URI")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    token_data = {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri}
    authorization_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"content-type": "application/x-www-form-urlencoded", "Authorization": f"Basic {authorization_b64}"}

    # Request access and refresh tokens
    print(code)
    print(client_id)
    print(redirect_uri)
    print(client_secret)
    res = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=headers)

    if res.status_code == 200:
        access_token = res.json()["access_token"]
        user_response = requests.get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {access_token}"})

        if user_response.status_code == 200:
            spotify_username = user_response.json()["email"]
            user = user_collection.find_one({"username": spotify_username})

            # Auth & XSRF Token
            auth_token = secrets.token_hex(16)
            auth_token_hash = hashlib.sha256(auth_token.encode()).hexdigest()
            xsrf_token = secrets.token_hex(16)

            if user == None:
                user_collection.insert_one({"username": spotify_username, "spotify_access_token": access_token, "xsrf_token": xsrf_token, "auth_token": auth_token_hash})
            else:
                user_collection.update_one({"username": spotify_username}, {"$set": {"spotify_access_token": access_token, "xsrf_token": xsrf_token, "auth_token": auth_token_hash}})

            return f"HTTP/1.1 302 Found\r\nLocation: /\r\nSet-Cookie: id={auth_token_hash};  Max-Age=3600; HttpOnly\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\n".encode()
        else:
            return f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nGetting Spotify User Info Failed".encode()
    else:
        return f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nX-Content-Type-Options: nosniff\r\n\r\nRequest access and refresh token failed".encode()
    


def spotifyPlaybackFunction(access_token):
    res = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers={"Authorization": f"Bearer {access_token}"})
    if res.status_code == 200:
        spotify_data = res.json()
        if spotify_data["is_playing"]: 
            track_name = spotify_data["item"]["name"]
            artist_name = spotify_data["item"]["artists"][0]["name"]
            return f" - Listening to '{track_name}' by {artist_name}"
        else:
            return " - Not listening to a song"
    else:
        return " - Not listening to a song"

