import React from "react";
import LineChart from "./LineChart";

interface StockData {
  [date: string]: {
    "open": string;
    "high": string;
    "low": string;
    "close": string;
    "volume": string;
  };
}

interface StockChartProps {
  stockData: StockData;
}

const StockChart: React.FC<StockChartProps> = ({ stockData }) => {
  const data = Object.keys(stockData).map((date) => {
    return {
      date,
      open: parseFloat(stockData[date]["open"]),
      high: parseFloat(stockData[date]["high"]),
      low: parseFloat(stockData[date]["low"]),
    };
  });

  console.log('Stock Data:', stockData);
  console.log('Data:', data);

  return (
    <div className={"text-white z-50 flex justify-center items-center flex-col"}>
      <h1>Stock Chart</h1>
      <LineChart data={data} />
    </div>
  );
};

export default StockChart;
