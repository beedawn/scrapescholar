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
          <option key={option+index} value={option}>
            {option}
          </option>
        ))}
      </select>
    );
  };

export default DropdownSearchBox;
