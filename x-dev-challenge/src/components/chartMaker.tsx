// src/StockChart.js
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'tailwindcss/tailwind.css';

const StockChart = ({ symbol }) => {
  const [stockData, setStockData] = useState(null);

  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const response = await axios.get(
          `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=D4P0RORZRZQMECVT`
        );

        const dailyData = response.data['Time Series (Daily)'];

        // Extract data for chart
        const dates = Object.keys(dailyData).reverse(); // Reverse to show latest date first
        const closingPrices = dates.map((date) => parseFloat(dailyData[date]['4. close']));

        setStockData({ dates, closingPrices });
      } catch (error) {
        console.error('Error fetching stock data:', error);
      }
    };

    fetchStockData();
  }, [symbol]);

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-4">Stock Chart for {symbol}</h2>
      {stockData && (
        <Line
          data={{
            labels: stockData.dates,
            datasets: [
              {
                label: 'Closing Price',
                data: stockData.closingPrices,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
              },
            ],
          }}
        />
      )}
    </div>
  );
};

export default StockChart;
