import StockDataMap from "../StockDataMap.ts";

type StockChartProps = {
  stockData: StockDataMap;
}

const StockChart = ( {stockData}: StockChartProps ) => {
  return (
    <div className={"text-white z-50"}>
      <h1>Stock Chart</h1>
      {Object.keys(stockData).map((date) => {
        return (
          <div key={date}>
            <h2>{date}</h2>
            <ul>
              <li>Open: {stockData[date]["1. open"]}</li>
              <li>High: {stockData[date]["2. high"]}</li>
              <li>Low: {stockData[date]["3. low"]}</li>
              <li>Close: {stockData[date]["4. close"]}</li>
              <li>Volume: {stockData[date]["5. volume"]}</li>
            </ul>
          </div>
        );
      })}
    </div>
  );
}

export default StockChart;