from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import secrets
from datetime import datetime, timedelta
import threading

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEFAULT_EXPIRATION_HOURS'] = 1

file_lock = threading.Lock()
file_expirations = {}

def generate_unique_filename(filename):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(filename)
    return random_hex + ext

def create_upload_directory():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def get_expiration_date(expiration_hours):
    return datetime.now() + timedelta(hours=expiration_hours)

def delete_expired_files():
    with file_lock:
        now = datetime.now()
        expired_files = [filename for filename, expiration in file_expirations.items() if expiration < now]
        for filename in expired_files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.remove(file_path)
            del file_expirations[filename]
    threading.Timer(60, delete_expired_files).start()

delete_expired_files()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        create_upload_directory()
        filename = generate_unique_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        expiration_hours = int(request.form.get('expiration', app.config['DEFAULT_EXPIRATION_HOURS']))
        expiration_date = get_expiration_date(expiration_hours)
        file_expirations[filename] = expiration_date
        file_url = request.url_root + 'uploads/' + filename
        return jsonify({
            'message': 'File uploaded successfully',
            'file_url': file_url,
            'expiration_date': expiration_date.strftime('%Y-%m-%d %H:%M:%S')
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=False)
