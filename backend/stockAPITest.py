import requests

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=TSLA&apikey=D4P0RORZRZQMECVT'
r = requests.get(url)
data = r.json()


print(data)