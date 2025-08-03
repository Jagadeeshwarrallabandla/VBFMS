from flask import Flask, request, jsonify
import os
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/MoveFilesource_Folder', methods=['POST'])
def moveFile():
    data = request.get_json()
    filename = data.get('filename')
    print(f"Received filename: {filename}")

    # Source and Destination Paths For File Transfering
    source_path = f"C:/Users/jagad/Downloads/{filename}.pdf"
    destination_path = f"C:/Users/jagad/OneDrive/Desktop/{filename}.pdf"

    try:
        shutil.move(source_path, destination_path)
        print("File moved successfully.")
        return jsonify({'message': '✅  File moved successfully ✅'})
    except Exception as e:
        print(f" Error moving file: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
