import {useState, KeyboardEvent, ChangeEvent} from "react";

type SearchBarProps = {
  search: (term: string) => void;
};

const SearchBar = ({search}: SearchBarProps) => {
    const [searchTerm, setSearchTerm] = useState<string>('');

    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setSearchTerm(e.target.value);
    };

    const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            search(searchTerm);
            setSearchTerm('');
        }
    };

    return (
        <div className="relative w-full flex justify-center text-black">
            <input
                type="text"
                style={{
                    width: '65%',
                    margin: '0 auto',
                    display: 'block',
                    padding: '12px 24px',
                    paddingLeft: '48px',
                    borderRadius: '9999px',
                    border: '1px solid #d1d5db',
                    boxShadow: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
                    fontSize: '18px',
                    fontFamily: 'Judson, serif',
                }}
                placeholder="Search for Financial Keywords..."
                value={searchTerm}
                onChange={handleInputChange}
                onKeyDownCapture={handleKeyDown}
            />
        </div>
    );
};

export default SearchBar;