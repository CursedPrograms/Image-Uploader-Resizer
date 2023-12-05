import os
import requests
import time
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image

app = Flask(__name__)

def get_file_contents(repo_owner, repo_name, file_path):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    
    # Make a GET request to the GitHub API
    response = requests.get(api_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        
        # Decode the content of the file (assuming it's Base64 encoded)
        content = data.get('content', '')
        content = content.encode('ascii')  # GitHub API returns content as Base64-encoded string
        content = content.decode('base64')  # Python 2
        # content = base64.b64decode(content).decode('utf-8')  # Python 3
        
        return content
    else:
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        return None

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        upload_folder = 'input'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # Resize the image to 128x128
        resized_file_path = os.path.join(upload_folder, 'resized_' + file.filename)
        with Image.open(file) as img:
            img = img.resize((128, 128))
            img.save(resized_file_path)
        
        # Pause for 3 seconds
        time.sleep(3)
        
        # Redirect back to the upload page
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
