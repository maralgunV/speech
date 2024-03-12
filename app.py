import os
from flask import Flask, request, jsonify, send_file
from speech_brain.convert import enhancement
from speech_brain.convert import send_audio
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def handle_request():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route('/')
def home():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route('/api/data')
def get_data():
    return jsonify(data=[1, 2, 3])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # Log the filename
    print('Uploaded file:', file.filename)

    return 'File uploaded successfully'

file_path = '/Users/maralgun/projects/speech/enhancement/maralgun.wav'


@app.route('/get_file_info')
def get_file_info():
    file_name = file_path.split('/')[-1]  # Extract filename from file path
    file_size = os.path.getsize(file_path)  # Get file size
    return jsonify(filename=file_name, size=file_size)

@app.route('/get_file')
def get_file():
    enhanced_audio = enhancement(file_path)
    return send_audio(enhanced_audio)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
