import SearchBar from "./components/searchBar.tsx";
import {useState} from "react";
import {HashLoader} from "react-spinners";
import axios, {AxiosResponse, AxiosError} from "axios";
import ParticleBackground from "./components/ParticleBackground.tsx";
import StockChart from "./components/StockChart.tsx";
import StockDataMap from "./StockDataMap.ts";
import { motion } from 'framer-motion';
import obj from "./StockApiReturn.ts";


function App() {
    const [searchClicked, setSearchClicked] = useState<boolean>(false);
    const [searchTerm, setSearchTerm] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);
    const [stockData, setStockData] = useState<StockDataMap>({});
    const getSearchResults = async (term: string): Promise<string> => {
        // fetch data from the API
        try {
          const response: AxiosResponse = await axios.post("https://api.asahoo.dev/api/v1/search", {
              search_term: term,
          });
          console.log(response.data);
            return JSON.stringify(response.data) || '';
          }
          catch (error) {
            console.log(error);
            return '';
        }
        // await axios.post("https://api.asahoo.dev/api/v1/search", {
        //     search_term: term,
        // }).then((response: AxiosResponse) => {
        //
        // }).catch((error: AxiosError) => {
        //     console.log(error);
        // });
        // return '';
    }
    const getStockData = async (stock: string): Promise<StockDataMap> => {
        // fetch data from the API
      try {
        const response: AxiosResponse = await axios.post("https://api.asahoo.dev/api/v1/stock", {
            stock_name: stock,
            interval: 30,
        });
        console.log('Response.data received from Axios post request\n', JSON.stringify(response.data));
        return response.data || {}; // Return response data
    } catch (error) {
        console.log(error);
        return {}; // Return empty object in case of error
    }
    }

    const getPrediction = async (stock: string): Promise<StockDataMap> => {
        // fetch data from the API
      console.log('Getting prediction for stock:', stock, 'interval:', 30)
        await axios.post("https://api.asahoo.dev/api/v1/predict", {
            stock_name: stock,
            interval: 30,
        }).then((response: AxiosResponse) => {
            console.log('Response received from getPrediction',response.data);
            return response.data || {};
        }).catch((error: AxiosError) => {
            console.log(error);
        });
      console.log('No prediction data found')
        return {};
    }

    const handleSearch = async (term: string) => {
        setLoading(true);
        console.log(term);
        const searchResult = await getSearchResults(term);
        console.log('searchresult',searchResult);
        if(searchResult === '') {
          console.log('No search results found');
            setLoading(false);
            setStockData({});
            return;
        }
        const stockDataFromAPI = await getStockData(term);
        console.log('Stock data from API in handle search:\n', JSON.stringify(stockDataFromAPI));
        setStockData(stockDataFromAPI);
        console.log('Stock data in handle search:\n', JSON.stringify(stockData));
        const prediction = await getPrediction(term);
        console.log('Prediction data in handle search:\n', JSON.stringify(prediction));

      // setLoading(true);
      // setTimeout(() => {
        setLoading(false);
        // }, 3000);
        // setStockData(obj);
    };

    return (
        <>
            <ParticleBackground/>
          <div
            className={
              "text-white font-public-sans flex flex-col min-h-screen w-screen items-center justify-center"
            }
          >
            <div className={`z-10 ${searchClicked ? 'hidden' : 'flex flex-col items-center'}`}>
              <h1 className="text-4xl text-white font-public-sans mb-28">X Finance</h1>
            </div>
            <motion.div
              initial={{opacity: 0}}
              animate={{opacity: searchClicked ? 1 : 0}}
              transition={{duration: 0.5}}
              className={`fixed flex flex-col items-left top-0 left-0 md:text-5xl text-xl ${!searchClicked ? 'opacity-0' : 'text-gray-300 font-mono p-4'}`}
            >
              <p className={"md:text-6xl text-2xl font-bold font-public-sans text-white"}>X</p>
              <p>F</p>
              <p>I</p>
              <p>N</p>
              <p>A</p>
              <p>N</p>
              <p>C</p>
              <p>E</p>
            </motion.div>

            <SearchBar
              search={(term: string) => handleSearch(term)}
              searchTerm={searchTerm}
              setSearchTerm={(term: string) => setSearchTerm(term)}
              setSearchClicked={(clicked: boolean) => setSearchClicked(clicked)}
              searchClicked={searchClicked}
            />
            {loading && searchClicked && searchTerm.length > 0 && (
              <div
                className="fixed w-screen h-screen flex items-center justify-center bg-opacity-50"
                style={{zIndex: 9999}}
              >
                <HashLoader color="#ffffff" loading={true} size={50}/>
              </div>
            )}
            <div className={"flex flex-col"}>
            <div className={"w-full h-full flex flex-row flex wrap p-24 gap-8"}>
            {
                searchClicked && !loading && searchTerm.length > 0 && (
                <div className={"backdrop-blur-sm bg-white bg-opacity-5 p-4 rounded-xl"}>
                  {stockData == ({})? <p>No Data</p> : <StockChart stockData={stockData}/>}
                </div>
                )
            }
            <div className={"backdrop-blur-sm bg-white w-full bg-opacity-5 p-4 rounded-xl"}>
              <h1>Future Stock Price</h1>
            </div>
            </div>
              <div>
                <h1>Stock Prediction</h1>
              </div>
            </div>
          </div>
        </>
    );
}

export default App;
