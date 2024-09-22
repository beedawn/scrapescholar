import React from 'react';

interface SearchBoxProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
  rows?: number;
}
const SearchBox: React.FC<SearchBoxProps> =
  ({ value,
    onChange,
    placeholder = "Enter text...",
    className = '',
    disabled = false }) => {
    return (
      <input
        onChange={onChange}
        className={`text-black px-2 py-2 ${className}`}
        value={value}
        disabled={disabled}
        placeholder={placeholder}
      >
      </input>
    );
  };

export default SearchBox;
