import React from 'react';


interface DropdownSearchBoxProps {
  value: string;
  onDropdownChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  className?: string;
  valueArray:any[];
}
const DropdownSearchBox: React.FC<DropdownSearchBoxProps> =
  ({ value,
    onDropdownChange,
    className = '', 
    valueArray
  }) => {


    return (
      <select
        value={value}
        onChange={onDropdownChange}
        className={`text-black p-2 ${className}`}
      >
        {valueArray.map((option, index) => (
          option.search_id ?
          <option key={option+index} value={option.search_id}>
            {option.title}
          </option>: <option key={option+index} value={option}>
            {option}-1
          </option>
        ))}
      </select>
    );
  };

export default DropdownSearchBox;
