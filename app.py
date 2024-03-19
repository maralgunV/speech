from flask import Flask, request, jsonify, send_file
from speech_brain.convert import enhancement
from flask_cors import CORS
import secrets, os

app = Flask(__name__)
CORS(app)

def generate_random_name():
    return secrets.token_hex(8)


UPLOAD_FOLDER = '/Users/maralgun/projects/save_wav_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# file_path = ""

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
    global file_path

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    random_name = generate_random_name()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], random_name)
    file.save(file_path)

    try:
        enh_file = enhancement(file_path)
    except Exception as e:
        return f'Error processing file: {str(e)}'

    file_data = enh_file.read()
    if file.filename == '':
        return 'No selected file'

    file_size = len(file_data)

    return str(file_size)

file_path = '/Users/maralgun/projects/speech/enhancement/maralgun.wav'


@app.route('/get_file_info')
def get_file_info():
    global file_path
    file = enhancement(file_path)
    # with open("output.wav", "wb") as f:
    #     f.write(file.getvalue())
    file_data = file.read()
    file_size = len(file_data)

    file_name = file_path.split('/')[-1]

    return jsonify(filename=file_name, size=file_size)

@app.route('/get_file')
def get_file():
    global file_path
    file = enhancement(file_path)

    try:
        return send_file(file,as_attachment=True, download_name='output.wav', mimetype='audio/wav')
    except Exception as e:
        return str(e)

@app.route('/get_audio')
def get_audio():    
    global file_path
    print("file_path" + file_path)
    return send_file(file_path, mimetype='audio/wav')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
