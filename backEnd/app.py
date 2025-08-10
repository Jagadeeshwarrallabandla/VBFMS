from flask import Flask, request, jsonify
import os
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/move_file', methods=['POST'])
def move_file():
    try:
        data = request.get_json(force=True)

        filename = data.get('filename', '').strip()
        main_folder = data.get('mainfolder', '').strip()
        sub_folder = data.get('subfolder', '').strip()

        # Source is Downloads folder
        source_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        # OneDrive base path (adjust if your OneDrive folder has a different name)
        onedrive_path = os.path.join(os.path.expanduser("~"), "OneDrive")

        if not os.path.exists(onedrive_path):
            return jsonify({'error': f'OneDrive folder not found at {onedrive_path}'}), 404

        # Destination folder
        destination_dir = os.path.join(onedrive_path, main_folder)
        if sub_folder:
            destination_dir = os.path.join(destination_dir, sub_folder)

        os.makedirs(destination_dir, exist_ok=True)

        # Match file ignoring spaces and case
        matched_file = None
        spoken_name = filename.replace(" ", "").lower()

        for f in os.listdir(source_dir):
            base_name, ext = os.path.splitext(f)
            if base_name.replace(" ", "").lower() == spoken_name:
                matched_file = f
                break

        if not matched_file:
            return jsonify({'error': f'File "{filename}" not found in Downloads'}), 404

        # Move the file
        source_file_path = os.path.join(source_dir, matched_file)
        destination_file_path = os.path.join(destination_dir, matched_file)
        shutil.move(source_file_path, destination_file_path)

        return jsonify({
            'message': f'{matched_file} moved successfully to {main_folder}{"/" + sub_folder if sub_folder else ""}'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
