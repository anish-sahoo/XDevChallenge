import React from "react";
import LineChart from "./LineChart";

interface StockData {
  [date: string]: {
    "1. open": string;
    "2. high": string;
    "3. low": string;
    "4. close": string;
    "5. volume": string;
  };
}

interface StockChartProps {
  stockData: StockData;
}

const StockChart: React.FC<StockChartProps> = ({ stockData }) => {
  const data = Object.keys(stockData).map((date) => {
    return {
      date,
      open: parseFloat(stockData[date]["1. open"]),
      high: parseFloat(stockData[date]["2. high"]),
      low: parseFloat(stockData[date]["3. low"]),
    };
  });

  return (
    <div className={"text-white z-50"}>
      <h1>Stock Chart</h1>
      <LineChart data={data} />
    </div>
  );
};

export default StockChart;
