from flask import Flask, request, jsonify
import os
import shutil
from flask_cors import CORS
from send2trash import send2trash

app = Flask(__name__)
CORS(app)

# Move file from Downloads to OneDrive folders
@app.route('/move_file', methods=['POST'])
def move_file():
    try:
        data = request.get_json(force=True)
        filename = data.get('filename', '').strip()
        main_folder = data.get('mainfolder', '').strip()
        sub_folder = data.get('subfolder', '').strip()

        # Map some spoken words to real folder names
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

        # Path to Downloads
        source_dir = os.path.join(os.path.expanduser("~"), "Downloads")

        # OneDrive path
        onedrive_path = os.path.join(os.path.expanduser("~"), "OneDrive")
        if not os.path.exists(onedrive_path):
            return jsonify({'error': f'❌ OneDrive folder not found'}), 404

        # Capitalize subfolder words
        if sub_folder:
            sub_folder = " ".join(word.capitalize() for word in sub_folder.split())

        # Destination path
        destination_dir = os.path.join(onedrive_path, main_folder)
        if sub_folder:
            destination_dir = os.path.join(destination_dir, sub_folder)

        if not os.path.exists(destination_dir):
            return jsonify({'error': f'❌ Destination "{destination_dir}" does not exist'}), 404

        # Match filename ignoring spaces/case
        matched_file = None
        spoken_name = filename.replace(" ", "").lower()
        for f in os.listdir(source_dir):
            base_name, ext = os.path.splitext(f)
            if base_name.replace(" ", "").lower() == spoken_name:
                matched_file = f
                break

        if not matched_file:
            return jsonify({'error': f'❌ File "{filename}" not found in Downloads'}), 404

        # Move file
        shutil.move(os.path.join(source_dir, matched_file), os.path.join(destination_dir, matched_file))
        return jsonify({'message': f'✅ "{matched_file}" moved successfully to {main_folder}{"/" + sub_folder if sub_folder else ""}'}), 200

    except Exception as e:
        return jsonify({'error': f'❌ {str(e)}'}), 500


# Create a new folder in OneDrive
@app.route('/create_folder', methods=['POST'])
def create_folder():
    data = request.get_json()
    folder_name = data.get('foldername', '').strip()
    main_folder = data.get('mainfolder', '').strip()

    if not folder_name or not main_folder:
        return jsonify({'error': '❌ Folder name and main folder are required'}), 400

    formatted_foldername = " ".join(word.capitalize() for word in folder_name.split())

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

    onedrive_path = os.path.join(os.path.expanduser("~"), "OneDrive")
    destination_dir = os.path.join(onedrive_path, main_folder, formatted_foldername)

    try:
        os.makedirs(destination_dir, exist_ok=False)
        return jsonify({'message': f'✅ Folder "{formatted_foldername}" created successfully in {main_folder}'}), 200
    except FileExistsError:
        return jsonify({'error': f'❌ Folder "{formatted_foldername}" already exists in {main_folder}'}), 400
    except Exception as e:
        return jsonify({'error': f'❌ {str(e)}'}), 500


# Rename a file
@app.route('/rename_file', methods=['POST'])
def rename_file():
    data = request.json
    old_name = data.get('old_name', "").strip()
    new_name = data.get('new_name', "").strip()
    folder_path_spoken = data.get('folder', "").strip()

    if not old_name or not new_name or not folder_path_spoken:
        return jsonify({"error": "❌ Missing old_name, new_name, or folder"}), 400

    # Convert spoken path to real path
    base_dir = os.path.expanduser("~")
    folder_parts = [part.strip().title() for part in folder_path_spoken.split("/")]
    folder_path = os.path.join(base_dir, *folder_parts)

    if not os.path.exists(folder_path):
        return jsonify({"error": f'❌ Folder "{folder_path_spoken}" not found'}), 404

    found_file = None
    for file in os.listdir(folder_path):
        name, ext = os.path.splitext(file)
        if name.lower() == old_name.lower():
            found_file = file
            break

    if not found_file:
        return jsonify({"error": f'❌ File "{old_name}" not found in {folder_path_spoken}'}), 404

    old_path = os.path.join(folder_path, found_file)
    new_path = os.path.join(folder_path, new_name + os.path.splitext(found_file)[1])

    if os.path.exists(new_path):
        return jsonify({"error": f'❌ File "{new_name}" already exists in {folder_path_spoken}'}), 409

    os.rename(old_path, new_path)
    return jsonify({"message": f'✅ "{found_file}" renamed to "{os.path.basename(new_path)}" successfully in {folder_path_spoken}'}), 200


# Delete file to Recycle Bin
@app.route('/delete_file', methods=['POST'])
def delete_file():
    data = request.json
    filename = data.get('filename')
    mainfolder = data.get('mainfolder')
    subfolder = data.get('subfolder')

    if not filename or not mainfolder:
        return jsonify({"error": "❌ Filename and main folder are required"}), 400

    onedrive_path = os.path.join(os.path.expanduser("~"), "OneDrive")

    mainfolder = " ".join(word.capitalize() for word in mainfolder.split())
    if subfolder:
        subfolder = " ".join(word.capitalize() for word in subfolder.split())

    base_dir = os.path.join(onedrive_path, mainfolder)
    if subfolder:
        base_dir = os.path.join(base_dir, subfolder)

    if not os.path.exists(base_dir):
        return jsonify({"error": f'❌ Folder "{base_dir}" does not exist'}), 404

    target_file = None
    spoken_name = filename.replace(" ", "").lower()
    for file in os.listdir(base_dir):
        name, ext = os.path.splitext(file)
        if name.replace(" ", "").lower() == spoken_name:
            target_file = file
            break

    if not target_file:
        return jsonify({"error": f'❌ File "{filename}" not found in {base_dir}'}), 404

    try:
        send2trash(os.path.join(base_dir, target_file))
        return jsonify({"message": f'✅ "{target_file}" deleted successfully from {mainfolder}{"/" + subfolder if subfolder else ""}'}), 200
    except Exception as e:
        return jsonify({"error": f'❌ Failed to delete file: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
