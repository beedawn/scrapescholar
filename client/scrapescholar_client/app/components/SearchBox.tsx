import React from 'react';

interface SearchBoxProps {
  value:string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
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
    <textarea
      onChange={onChange}
      className={className}
      value={value}
      disabled={disabled}
      rows={rows}
      placeholder={placeholder}
      style={{color:'black'}}
    >
     
    </textarea>
  );
};

export default SearchBox;
