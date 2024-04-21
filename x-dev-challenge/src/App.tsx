import SearchBar from "./components/searchBar.tsx";
import { useState } from "react";
import { HashLoader } from "react-spinners";
import axios, {AxiosResponse, AxiosError} from "axios";
import ParticleBackground from "./components/ParticleBackground.tsx";
import obj from "./StockApiReturn.ts";
import StockChart from "./components/StockChart.tsx";
import StockDataMap from "./StockDataMap.ts";

function App() {
  const [searchClicked, setSearchClicked] = useState<boolean>(false);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const [stockData, setStockData] = useState<StockDataMap>({});
  const getSearchResults = async (term: string) => {
    // fetch data from the API
    await axios.post("http://localhost:5000/api/v1/search", {
      search_term: term,
    }).then((response: AxiosResponse) => {
      console.log(response.data);
    }).catch((error: AxiosError) => {
      console.log(error);
    });
  }
  const getStockData = async (stock: string) => {
    // fetch data from the API
    await axios.post("http://localhost:5000/api/v1/stock", {
      stock_name: stock,
      interval: 30,
    }).then((response: AxiosResponse) => {
      console.log(response.data);
    }).catch((error: AxiosError) => {
      console.log(error);
    });
  }

  const handleSearch = async (term: string) => {
    setLoading(true);
    console.log(term);
    await getSearchResults(term);
    // const stockDataFromAPI = await getStockData(term);
    // setStockData(stockDataFromAPI);
    setLoading(false);
    setStockData(obj);
  };

  return (
    <>
      <ParticleBackground/>
      <div
        className={
          "text-white font-public-sans flex flex-col min-h-screen w-screen items-center justify-center"
        }
      >

        <SearchBar
          search={(term: string) => handleSearch(term)}
          searchTerm={searchTerm}
          setSearchTerm={(term: string) => setSearchTerm(term)}
          setSearchClicked={(clicked: boolean) => setSearchClicked(clicked)}
          searchClicked={searchClicked}
        />
        {loading && searchClicked && searchTerm.length > 0 && (
        <div
          className="fixed top-0 left-0 w-screen h-screen flex items-center justify-center bg-opacity-50"
          style={{ zIndex: 9999 }}
        >
          <HashLoader color="#ffffff" loading={true} size={50} />
        </div>
      )}
        {
          stockData && (
            <StockChart stockData={stockData}/>)
        }
      </div>
    </>
  );
}

export default App;
