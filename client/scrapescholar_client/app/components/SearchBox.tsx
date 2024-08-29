import React from 'react';

interface SearchBoxProps {
  value:string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  className?: string;
  disabled?: boolean;
  rows?: number;
}

const SearchBox: React.FC<SearchBoxProps> = 
({ value, 
    onChange,
    placeholder="Enter text...", 
    rows=1,
    className='',
    disabled=false }) => {
  return (
    <input
      onChange={onChange}
      className={className}
      value={value}
      disabled={disabled}
      placeholder={placeholder}
      style={{color:'black'}}
    >
     
    </input>
  );
};

export default SearchBox;
