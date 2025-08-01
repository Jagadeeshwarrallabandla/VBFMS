from flask import Flask, jsonify 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/SuccessFullMessage', methods=['GET'])
def message():
    return jsonify({"message": "✅ Backend Connected Successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
