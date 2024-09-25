import React from 'react';
import DropdownType from '../../types/DropdownType'
interface DropdownSearchBoxProps {
  value: string;
  onDropdownChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
  className?: string;

}
const DropdownSearchBox: React.FC<DropdownSearchBoxProps> =
  ({ value,
    onDropdownChange,
    className = ''
  }) => {
    return (
      <select
        value={value}
        onChange={onDropdownChange}
        className={`text-black p-2 ${className}`}
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
