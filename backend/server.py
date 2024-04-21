import os
from quart import Quart, jsonify, request
from dotenv import load_dotenv
from quart_cors import cors
from groktest import get_terms
from stockdata import getStockData

load_dotenv()

app = Quart(__name__)
app = cors(app, allow_origin=["http://localhost:5173", "http://0.0.0.0:5173", "http://127.0.0.1:5173", "https://finance.asahoo.dev", "https://api.asahoo.dev"])


@app.route('/')
async def hello():
    return 'Hello, World! This is my Flask application. This endpoint should not be called.'


@app.route('/api/v1/search', methods=['POST'])
async def test():
    if request.method == 'POST':
        data = await request.get_json()

        print(data)
        terms = await get_terms(data.get('search_term'))
        print(terms)
        response = jsonify({'result': f'{terms}'})
        response.headers.add('Access-Control-Allow-Origin', '*')  # Add CORS header
        return response
    return jsonify({'error': 'Method not allowed'}), 405


@app.route('/api/v1/stock', methods=['POST'])
async def stockdata():
    if request.method == 'POST':
        data = await request.get_json()
        print('JSON input', data)
        try:
            stock_data = getStockData(data.get('stock_name'), data.get('interval'))
            response = jsonify(stock_data)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        except Exception as e:
            print(e)
            return jsonify({'error': f'Error fetching stock data {e}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=int(os.environ.get('PORT', 4998)))
