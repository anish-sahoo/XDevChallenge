import os
from quart import Quart, jsonify, request
from dotenv import load_dotenv
from quart_cors import cors
from groktest import get_terms, gen_predictions, gen_short
from searchAllTest import get_all_tweets
from stockdata import getStockData
import json

load_dotenv()

app = Quart(__name__)
app = cors(app, allow_origin="*")


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


@app.route('/api/v1/predict', methods=['POST'])
async def predict():
    if request.method == 'POST':
        data = await request.get_json()
        print('JSON input', data)
        try:
            stock_name = data.get('stock_name')
            print('Stock name:', stock_name)
            terms = await get_terms(stock_name)
            print('Terms:', terms)
            stock_data = getStockData(data.get('stock_name'), data.get('interval'))
            print('Stock data:', stock_data)
            tweets_list = get_all_tweets(terms)
            print('Tweets:', tweets_list)
            prediction = await gen_short(tweets_list, stock_data, stock_name)
            print('Gen Short>>>>>>>', prediction)
#            prediction2 = await gen_long(tweets_list, stock_data, stock_name)
#            print('Gen Long>>>>>>>', prediction2)
            prediction3 = await gen_predictions(tweets_list, stock_data, stock_name)
            print('Gen Predictions>>>>>>>', prediction3)
#            prediction4 = await gen_old_predictions(tweets_list, stock_data, stock_name)
#            print('Gen Old Predictions>>>>>>>', prediction4)
            return prediction
        except Exception as e:
            print('Exception',e)
            return jsonify({'error': f'Error fetching prediction {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=int(os.environ.get('PORT', 4998)))
