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

        # Map spoken main folder names to actual folder names
        folder_map = {
            "desktop": "Desktop",
            "desk": "Desktop",
            "documents": "Documents",
            "document": "Documents",
            "pictures": "Pictures",
            "picture": "Pictures",
            "downloads": "Downloads",
            "download": "Downloads"
        }
        main_folder = folder_map.get(main_folder.lower(), main_folder)

        # Source is Downloads
        source_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        # OneDrive base path
        onedrive_path = os.path.join(os.path.expanduser("~"), "OneDrive")

        if not os.path.exists(onedrive_path):
            return jsonify({'error': f'OneDrive folder not found at {onedrive_path}'}), 404

        # Capitalize each word in subfolder for matching
        if sub_folder:
            sub_folder = " ".join(word.capitalize() for word in sub_folder.split())

        # Destination folder path
        destination_dir = os.path.join(onedrive_path, main_folder)
        if sub_folder:
            destination_dir = os.path.join(destination_dir, sub_folder)

        # Ensure destination exists
        if not os.path.exists(destination_dir):
            return jsonify({'error': f'❌ Destination folder "{destination_dir}" does not exist.'}), 404

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
            'message': f'✅ {matched_file} moved successfully to {main_folder}/{sub_folder}'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# ---------------- CREATE FOLDER ROUTE ----------------
@app.route('/create_folder', methods=['POST'])
def create_folder():
    data = request.get_json()

    folder_name = data.get('foldername', '').strip()
    main_folder = data.get('mainfolder', '').strip()

    if not folder_name or not main_folder:
        return jsonify({'error': 'Folder name and main folder are required'}), 400

    # Capitalize each word for proper formatting
    formatted_foldername = " ".join(word.capitalize() for word in folder_name.split())

    # Map common speech variations for main folder
    folder_map = {
        "desktop": "Desktop",
        "desk": "Desktop",
        "documents": "Documents",
        "document": "Documents",
        "pictures": "Pictures",
        "picture": "Pictures",
        "downloads": "Downloads",
        "download": "Downloads"
    }
    main_folder = folder_map.get(main_folder.lower(), main_folder)

    # OneDrive base path
    onedrive_path = os.path.join(os.path.expanduser("~"), "OneDrive")

    # Destination main folder
    destination_dir = os.path.join(onedrive_path, main_folder)

    # ✅ Use formatted_foldername in path so actual folder is created with capitalized words
    new_folder_path = os.path.join(destination_dir, formatted_foldername)
    print(f"Newly Created Folder name is {formatted_foldername} in {main_folder}")

    try:
        os.makedirs(new_folder_path, exist_ok=False)  # Fail if already exists
        return jsonify({'message': f'✅ Folder "{formatted_foldername}" created successfully in {main_folder}.'})
    except FileExistsError:
        return jsonify({'error': f'❌ Folder "{formatted_foldername}" already exists in {main_folder}.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
