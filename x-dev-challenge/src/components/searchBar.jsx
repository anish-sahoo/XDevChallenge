import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const SearchBar = ({ languages }) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [matchedLanguages, setMatchedLanguages] = useState([]);
  const [dropdownVisible, setDropdownVisible] = useState(false);
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const term = e.target.value;
    setSearchTerm(term);

    // Filter languages based on the search term
    const matched = languages.filter((lang) =>
      lang.toLowerCase().includes(term.toLowerCase()),
    );
    setMatchedLanguages(matched);
    setDropdownVisible(true);
  };

  const handleLanguageSelection = (language) => {
    setSearchTerm(language);
    navigate(`/chatType?language=${language}`);
    setDropdownVisible(false);
    // Trigger search automatically when language is selected
    console.log("Searching for language:", language);
  };

  return (
    <div className="relative w-full flex justify-center">
      <input
        type="text"
        style={{
          width: '85%',
          margin: '0 auto',
          display: 'block',
          padding: '12px 24px',
          paddingLeft: '48px', // Increase padding-left to avoid text overlapping the icon
          backgroundImage: 'url(/Search111.png)',
          backgroundPosition: '5px center', // Adjust as necessary
          backgroundRepeat: 'no-repeat',
          backgroundSize: '48px 48px',
          borderRadius: '9999px',
          border: '1px solid #d1d5db',
          boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
          fontSize: '18px',
          fontFamily: 'Judson, serif',
        }}
        placeholder="Search for languages..."
        value={searchTerm}
        onChange={handleInputChange}
      />
      {dropdownVisible && matchedLanguages.length > 0 && (
        <div
          className="absolute top-full left-0 z-10 w-full bg-white shadow-lg
                        rounded-xl border border-gray-300 overflow-hidden"
          style={{ fontFamily: 'Judson, serif' ,
          width: '80%', // Adjust the width as needed
          left: '10%', // Center the dropdown relative to the search bar
          right: '7.5%',
          }} // Apply Judson font to the entire dropdown

        >
          {matchedLanguages.slice(0,5).map((language, index) => (
            <div
              key={index}
              className="py-2 px-4 hover:bg-gray-100 cursor-pointer"
              onClick={() => handleLanguageSelection(language)}
            >
              {language}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchBar;