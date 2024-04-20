import SearchBar from "./components/searchBar.tsx";
function App() {
  return (
    <>
      <div
        className={
          "bg-black text-white font-public-sans flex h-screen w-screen items-center justify-center"
        }
      >
        <SearchBar search={(term: string) => console.log(term)} />
      </div>
    </>
  );
}

export default App;
