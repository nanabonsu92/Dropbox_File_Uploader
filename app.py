from flask import Flask, request, jsonify, render_template
import dropbox
import os
import auth
import dropbox_client

app = Flask(__name__)

# Dropbox access token (ensure you handle this securely in production)
ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    try:
        # Save file temporarily
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, file.filename)
        file.save(file_path)

        # Upload file to Dropbox
        with open(file_path, 'rb') as f:
            dbx.files_upload(f.read(), f'/{file.filename}', mute=True)

        # Generate shared link
        link = dbx.sharing_create_shared_link_with_settings(
            f'/{file.filename}')
        download_link = link.url.replace('?dl=0', '?dl=1')

        # Clean up temporary file
        os.remove(file_path)

        return jsonify({'success': True, 'link': download_link})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/list_files', methods=['GET'])
def list_files():
    folder_path = request.args.get('folder_path', '')
    try:
        files = dropbox_client.list_files(ACCESS_TOKEN, folder_path)
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
