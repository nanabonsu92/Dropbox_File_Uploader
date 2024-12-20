# auth.py
import requests


def get_authorization_url(app_key, redirect_uri):
    auth_url = f"https://www.dropbox.com/oauth2/authorize?client_id={app_key}&response_type=code&redirect_uri={redirect_uri}"
    return auth_url


def get_access_token(auth_code, app_key, app_secret, redirect_uri):
    token_url = 'https://api.dropboxapi.com/oauth2/token'
    token_data = {
        'code': auth_code,
        'grant_type': 'authorization_code',
        'client_id': app_key,
        'client_secret': app_secret,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(token_url, data=token_data)

    # Check response
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print(f"Access Token: {access_token}")
        return access_token
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
