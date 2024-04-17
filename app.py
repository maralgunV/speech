from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import secrets, os
import time
from speech_brain.unzip import unzip_from_file, read_files_in_folder, zip_folder, create_zip_from_files
from speech_brain.convert import enhancement

app = Flask(__name__)
CORS(app)

def generate_random_name():
    timestamp_now = str(int(time.time()))
    return secrets.token_hex(8) + timestamp_now


UPLOAD_FOLDER = '/Users/maralgun/projects/save_wav_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/api/data')
def get_data():
    return jsonify(data=[1, 2, 3])

@app.route('/modelId', methods=['POST'])
def index():
    global modelId
    modelId = request.form.get('data')
    return 'Model ID received successfully.'


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
        enh_file = enhancement(file_path, modelId)
    except Exception as e:
        return f'Error processing file: {str(e)}'

    file_data = enh_file.read()
    if file.filename == '':
        return 'No selected file'

    file_size = len(file_data)

    return str(file_size)

file_path = '/Users/maralgun/projects/speech/enhancement/maralgun.wav'
modelId = 2

@app.route('/get_file_info')
def get_file_info():
    global file_path
    file = enhancement(file_path, modelId)
    # with open("output.wav", "wb") as f:
    #     f.write(file.getvalue())
    file_data = file.read()
    file_size = len(file_data)

    file_name = file_path.split('/')[-1]

    return jsonify(filename=file_name, size=file_size)

@app.route('/get_file')
def get_file():
    global file_path
    file = enhancement(file_path, modelId)

    try:
        return send_file(file,as_attachment=True, download_name='output.wav', mimetype='audio/wav')
    except Exception as e:
        return str(e)

@app.route('/get_audio')
def get_audio():    
    global file_path
    print("file_path" + file_path)
    return send_file(file_path, mimetype='audio/wav')

folder_dir = "/Users/maralgun/projects/save_folders"
unzip_folder = folder_dir

@app.route('/uploadZip', methods=['POST'])
def upload_file_zip():
    global unzip_folder

    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'
    
    folder_name = generate_random_name()
    unzip_folder = os.path.join(folder_dir, folder_name)
    print(unzip_folder)
    
    # file.filename = folder_name + '.zip'
    unzip_from_file(file, folder_dir, folder_name)


    return file.filename   

@app.route('/get_file_zip')
def get_file_zip():

    # print(unzip_folder)
    # print(modelId)
    files = read_files_in_folder(unzip_folder, modelId)
    # file = zip_folder(unzip_folder)
    file = create_zip_from_files(files)


    try:
        return send_file(file, as_attachment=True, download_name='output.zip', mimetype='zip')
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
