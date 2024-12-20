# main.py
import auth
import dropbox_client
import json

# Constants
app_key = 'replace_with_app_key'
app_secret = 'replace_with_app_secret'
redirect_uri = 'http://localhost:8080'

if __name__ == '__main__':
    # Get authorization URL and prompt user
    auth_url = auth.get_authorization_url(app_key, redirect_uri)
    # Correct string formatting
    print(f"Please go to this URL and authorize the app: {auth_url}")
    auth_code = input("Paste the authorization code here: ")

    # Get access token
    access_token = auth.get_access_token(
        auth_code, app_key, app_secret, redirect_uri)

    if access_token:
        # Get user account information
        user_info = dropbox_client.get_user_account_info(access_token)
        if user_info:
            print("User Account Information:")
            print(json.dumps(user_info, indent=4))
        else:
            print("Failed to retrieve user account information.")

    # Example: Upload a file to Dropbox (e.g., "image.jpg" to "/image.jpg")
        # Path to the image on your local system
        file_path = "C:/Users/Kwaku Bonsu-Afrane/Desktop/SOA/task-2/images.jfif"
        destination_path = '/image.jpg'  # Path where you want to store it in Dropbox
        response = dropbox_client.upload_file(
            access_token, file_path, destination_path)

        if response:
            print("Upload successful. File details:")
            print(json.dumps(response, indent=4))
        else:
            print("Failed to upload the file.")

        # List files in a folder
        folder_path = input(
            "Enter the Dropbox folder path to list files (e.g., '') for root: ")
        files = dropbox_client.list_files(access_token, folder_path)

        if files:
            print(f"Files in folder '{folder_path}':")
            for file in files:
                # Pretty-printing each file's details
                print(json.dumps(file, indent=4))
        else:
            print(
                f"No files found or failed to list files in folder: {folder_path}")

    else:
        print("Failed to obtain access token.")
