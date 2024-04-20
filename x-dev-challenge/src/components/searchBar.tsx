import { KeyboardEvent, ChangeEvent } from "react";
import { motion } from "framer-motion";

type SearchBarProps = {
  search: (term: string) => void;
  searchClicked: boolean;
  setSearchClicked: (clicked: boolean) => void;
  searchTerm: string;
  setSearchTerm: (term: string) => void;
};

const SearchBar = ({
  search,
  searchClicked,
  setSearchClicked,
  searchTerm,
  setSearchTerm,
}: SearchBarProps) => {
  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      search(searchTerm);
      setSearchClicked(searchTerm.length > 0);
    }
  };

  return (
    <motion.div
      className="relative w-full flex justify-center text-black"
      initial={{ y: 0 }}
      animate={{ y: searchClicked && searchTerm.length > 0 ? "-40vh" : 0 }} // Move up when searchTerm is not empty
      transition={{ type: "spring", duration: 0.5 }} // Adjust the transition type and duration
    >
      <input
        type="text"
        style={{
          width: "65%",
          margin: "0 auto",
          display: "block",
          padding: "12px 24px",
          paddingLeft: "48px",
          borderRadius: "9999px",
          border: "1px solid #d1d5db",
          boxShadow: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
          fontSize: "18px",
        }}
        placeholder="Search for Financial Keywords..."
        value={searchTerm}
        onChange={handleInputChange}
        onKeyDownCapture={handleKeyDown}
      />
    </motion.div>
  );
};

export default SearchBar;
