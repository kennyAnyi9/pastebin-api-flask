# app.py
from flask import Flask, request, jsonify
from database import create_paste, get_paste
from flask_cors import CORS


CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000", "https://pasteit.vercel.app"}})
app = Flask(__name__)

@app.route('/api/paste', methods=['POST'])
def create_paste_route():
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    paste_id = create_paste(content)
    url = f"https://pastebin-7j39.onrender.com/api/paste/{paste_id}"  # Update this for production
    return jsonify({'url': url}), 201

@app.route('/api/paste/<paste_id>', methods=['GET'])
def get_paste_content(paste_id):
    content = get_paste(paste_id)
    if content:
        return jsonify({'content': content})
    return jsonify({'error': 'Paste not found'}), 404

if __name__ == '__main__':
    app.run()  # FLASK_ENV in .flaskenv will handle debug mode