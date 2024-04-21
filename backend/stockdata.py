from datetime import datetime, timedelta

import requests

api_key = 'BX21JNURWAU8G8ZM'
api_key_will = 'D4P0RORZRZQMECVT'
api_key_will2 = '9SM5Z7ADUI0PCY1Q'


def getStockData(symbol, interval):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + f'&apikey={api_key_will2}'
    r = requests.get(url)
    json_data = r.json()

    print('JSON in getStockData:', json_data)

    last_refreshed_date_str = json_data['Meta Data']['3. Last Refreshed']
    last_refreshed_date = datetime.strptime(last_refreshed_date_str, '%Y-%m-%d')

    # Calculate the date 30 days ago from the last refreshed date
    thirty_days_ago = last_refreshed_date - timedelta(days=interval)

    # Extract stock data for the last 30 days
    last_30_days_data = {}
    for date_str, data in json_data['Time Series (Daily)'].items():
        date = datetime.strptime(date_str, '%Y-%m-%d')
        if thirty_days_ago <= date <= last_refreshed_date:
            last_30_days_data[date_str] = data

    return last_30_days_data
