import os
import zipfile
from speech_brain.convert import enhancement
import io

def unzip_from_file(file_obj, extract_to_directory, folder_name):
    # extract_to_directory = os.path.join(extract_to_directory, folder_name)
    os.makedirs(extract_to_directory, exist_ok=True)
    
    unzip(file_obj, extract_to_directory)
    filename_without_extension = os.path.splitext(file_obj.filename)[0]
    os.rename(os.path.join(extract_to_directory, filename_without_extension), os.path.join(extract_to_directory, folder_name))


def unzip(zip_file_obj, extract_to_directory):
    """
    Unzips the specified zip file to the specified directory,
    excluding the __MACOSX folder if present.

    Args:
        zip_file_obj (werkzeug.datastructures.FileStorage): File object representing the zip file.
        extract_to_directory (str): Directory where the contents will be extracted.

    Returns:
        None
    """
    with zipfile.ZipFile(zip_file_obj, 'r') as zip_ref:
        for member in zip_ref.infolist():
            # Skip extracting the __MACOSX folder
            if '__MACOSX' in member.filename:
                continue
            zip_ref.extract(member, extract_to_directory)
    print("Zip file extracted successfully.")


def read_files_in_folder(folder_path, id):
    enhanced_files = {}
    file_count = 0
    print("READ FILES IN FOLDER")
    for filename in os.listdir(folder_path):
        if filename == '.DS_Store':
            continue  # Skip .DS_Store files
        file_count += 1
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")
        if os.path.isfile(file_path):
            enhanced_audio = enhancement(file_path, id)
            enhanced_files[filename] = enhanced_audio
    print(f"Total files processed: {file_count}")
    return enhanced_files


def create_zip_from_files(files):
    """
    Creates a ZIP file containing the provided files.

    Args:
        files (dict): A dictionary containing file names as keys and file contents as values.

    Returns:
        io.BytesIO: A BytesIO object containing the ZIP file data.
    """
    zip_file = io.BytesIO()
    with zipfile.ZipFile(zip_file, mode='w') as zf:
        for filename, enhanced_audio in files.items():
            # Extract bytes from enhanced_audio (_io.BytesIO object)
            audio_bytes = enhanced_audio.getvalue()
            # Write the bytes to the ZIP file
            zf.writestr(filename, audio_bytes)
    # Reset the BytesIO object pointer
    zip_file.seek(0)
    return zip_file

def zip_folder(folder_path):
    """
    Creates a zip file containing all the files in the specified folder.

    Args:
        folder_path (str): Path to the folder containing the files.

    Returns:
        io.BytesIO: A BytesIO object containing the zip file data.
    """
    # Create a BytesIO object to hold the zip file data
    zip_buffer = io.BytesIO()

    # Create a zip file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Iterate over all files in the folder
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Get the full path of the file
                file_path = os.path.join(root, file)
                # Add the file to the zip file with the relative path
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

    # Reset the buffer pointer to the beginning
    zip_buffer.seek(0)

    return zip_buffer
