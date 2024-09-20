import React, {useState} from 'react';


import Button from './Button';
import { ResultItem } from '../views/SearchView';
interface SortToggleButtonProps {


handleSort:(field:keyof ResultItem, sortDirection:string)=>void;
field:keyof ResultItem;
}
const SortToggleButton: React.FC<SortToggleButtonProps> = ({handleSort, field}) => {
    const[pressed, setPressed]= useState(false);
  
    const handlePress=(field:keyof ResultItem, direction:string)=>{
        handleSort(field, direction)
        setPressed(!pressed)

    }
  
    return (
  

                    <div>
                    {pressed?<Button onClick={()=>handlePress(field, "asc")}>up</Button>:<Button onClick={()=>handlePress(field,"desc")}>down</Button>}
                    </div>
    )
};

export default SortToggleButton;
