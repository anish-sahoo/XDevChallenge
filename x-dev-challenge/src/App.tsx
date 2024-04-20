import SearchBar from "./components/searchBar.tsx";
import Card from "./components/card.tsx";

function App() {
    return (
        <>
            <div
                className={
                    "bg-zinc-900 text-white font-public-sans flex flex-col min-h-screen w-screen items-center justify-center"
                }
            >
                <SearchBar search={(term: string) => console.log(term)}/>
                <Card/>
            </div>
        </>
    );
}

export default App;
