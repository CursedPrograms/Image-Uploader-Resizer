import os
import requests
import time
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image

app = Flask(__name__)

def get_file_contents(repo_owner, repo_name, file_path):
    api_url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}'
    
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        content = data.get('content', '')
        content = content.encode('ascii') 
        content = content.decode('base64')  
        return content
    else:
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

        resized_file_path = os.path.join(upload_folder, 'resized_' + file.filename)
        with Image.open(file) as img:
            img = img.resize((128, 128))
            img.save(resized_file_path)
            
        time.sleep(3)

        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
