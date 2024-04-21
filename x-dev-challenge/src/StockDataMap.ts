interface StockData {
  "open": string;
  "high": string;
  "low": string;
  "close": string;
  "volume": string;
}

type StockDataMap = {
  [date: string]: StockData;
}

export default StockDataMap;