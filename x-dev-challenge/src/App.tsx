import SearchBar from "./components/searchBar.tsx";
import { useState } from "react";
import { HashLoader } from "react-spinners";

function App() {
  const [searchClicked, setSearchClicked] = useState<boolean>(false);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleSearch = (term: string) => {
    setLoading(true);
    console.log(term);
    setTimeout(() => {
      setLoading(false);
    }, 4000);
  };

  return (
    <>
      <div
        className={
          "bg-zinc-900 text-white font-public-sans flex flex-col min-h-screen w-screen items-center justify-center items-center"
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
          <div>
            <HashLoader
              cssOverride={{ display: "block", margin: "0 auto" }}
              color="#ffffff"
              loading={true}
              size={50}
            />
          </div>
        )}
      </div>
    </>
  );
}

export default App;
