import React from 'react';
import DropdownType from '../types/DropdownType'
interface DropdownSearchBoxProps {
  value:string;
  onDropdownChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;

  placeholder?: string;
  className?: string;
  disabled?: boolean;
  rows?: number;
}

const DropdownSearchBox: React.FC<DropdownSearchBoxProps> = 
({ value, 
    onDropdownChange,
    placeholder="Enter text...", 
    rows=1,
    className='',

    disabled=false }) => {
  return (
    <select
    value={value}
    onChange={onDropdownChange}
    className={className}
    disabled={disabled}
    style={{ marginLeft: '8px', color: 'black'}} 
  >
    {Object.values(DropdownType).map((option) => (
      <option key={option} value={option}>
        {option}
      </option>
    ))}
  </select>
  );
};

export default DropdownSearchBox;
