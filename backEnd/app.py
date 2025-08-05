from flask import Flask, request, jsonify
import os
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/MoveFilesource_Folder', methods=['POST'])
def moveFile():
    data = request.get_json()
    input_filename = data.get('filename', '').strip().lower()
    print(f"Received input filename: {input_filename}")

    source_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    destination_dir = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")  

    files_in_downloads = os.listdir(source_dir)

    matched_file = None
    for f in files_in_downloads:
        base_name, ext = os.path.splitext(f)
        if base_name.lower() == input_filename:
            matched_file = f
            break

    if matched_file:
        source_file_path = os.path.join(source_dir, matched_file)
        print(f"The Original File Location : {source_file_path}")
        destination_file_path = os.path.join(destination_dir, matched_file)
        print(f"Moved Files Location : {destination_file_path}")
        

        try:
            shutil.move(source_file_path, destination_file_path)
            print(f"Moved file: {matched_file}")
            return jsonify({'message': f'{matched_file} moved successfully to Desktop'})
        except Exception as e:
            print(f"Error moving file: {e}")
            return jsonify({'error': f'Error moving file: {str(e)}'}), 500
    else:
        print("File not found in Downloads folder.")
        return jsonify({'error': 'File not found in Downloads folder'}), 404

if __name__ == '__main__':
    app.run(debug=True)
