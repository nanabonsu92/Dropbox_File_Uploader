# dropbox_client.py
import requests
import json


def get_user_account_info(access_token):
    user_info_url = 'https://api.dropboxapi.com/2/users/get_current_account'
    headers = {
        # No need for Content-Type header here
        'Authorization': f'Bearer {access_token}',
    }

    # Sending a POST request to the Dropbox API to get user account information
    response = requests.post(user_info_url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Return the JSON response containing the user's account info
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def upload_file(access_token, file_path, destination_path):
    upload_url = 'https://content.dropboxapi.com/2/files/upload'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream',
        'Dropbox-API-Arg': json.dumps({
            "path": destination_path,
            "mode": "add",
            "autorename": True,
            "mute": False,
            "strict_conflict": False
        }),
    }

    with open(file_path, 'rb') as f:
        data = f.read()

    response = requests.post(upload_url, headers=headers, data=data)

    if response.status_code == 200:
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            print("Error decoding JSON:", response.text)
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None


def list_files(access_token, folder_path):
    list_folder_url = 'https://api.dropboxapi.com/2/files/list_folder'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    data = {
        "path": folder_path,
        "recursive": False
    }

    response = requests.post(list_folder_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get('entries', [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
