from datetime import datetime, timedelta, timezone

import requests

api_key = 'BX21JNURWAU8G8ZM'
api_key_will = 'D4P0RORZRZQMECVT'
api_key_will2 = '9SM5Z7ADUI0PCY1Q'
api_key_tmm = 'D7S4E7R5MBJSZMEO'


def getStockData(symbol, interval):
    thirty_days_ago = datetime.now(tz=timezone.utc) - timedelta(days=interval)
    url = "https://api.twelvedata.com/time_series?apikey=78e803f08d044ca7b698dc327a60b3c9&interval=1day&symbol=" + symbol + "&type=stock&timezone=utc&format=JSON&start_date=" + thirty_days_ago.strftime("%Y-%m-%d")
    print('URL in getStockData:', url)
    r = requests.get(url)
    json_data = r.json()

    # print('JSON in getStockData:', json_data)

    # last_refreshed_date_str = json_data['Meta Data']['3. Last Refreshed']
    # last_refreshed_date = datetime.strptime(last_refreshed_date_str, '%Y-%m-%d')

    # Calculate the date 30 days ago from the last refreshed date
    # thirty_days_ago = last_refreshed_date - timedelta(days=interval)

    # Extract stock data for the last 30 days
    last_30_days_data = {}
    for dict in json_data['values']:

        date = dict["datetime"]
        dict.pop("datetime")
        last_30_days_data[date] = dict

    return last_30_days_data
def main():
    stock_data = getStockData('LMT', 30)
    print(stock_data)
main()
