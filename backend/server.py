import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin


load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World! This is my Flask application. This endpoint should not be called.'


@app.route('/api/v1/search', methods=['POST'])
@cross_origin()
def test():
    if request.method == 'POST':
        data = request.get_json()
        print(data.get('search_term'))
        return jsonify({'message': f'{data.get("search_term", "No search term provided")}'})

    return jsonify({'error': 'Method not allowed'}), 405


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT', 5000), host='0.0.0.0')
