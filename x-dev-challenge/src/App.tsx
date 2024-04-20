import SearchBar from "./components/searchBar.tsx";
import { useState } from "react";

function App() {
  const [searchClicked, setSearchClicked] = useState<boolean>(false);

  return (
    <>
      <div
        className={
          "bg-zinc-900 text-white font-public-sans flex flex-col min-h-screen w-screen items-center justify-center items-center"
        }
      >
        <SearchBar
          search={(term: string) => {
            console.log(term);
          }}
          setSearchClicked={(clicked: boolean) => setSearchClicked(clicked)}
          searchClicked={searchClicked}
        />
        {searchClicked && <div className="text-2xl">Search clicked</div>}
      </div>
    </>
  );
}

export default App;
