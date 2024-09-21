import React, {useState} from 'react';


import Button from './Button';
import { ResultItem } from '../views/SearchView';
interface SortToggleButtonProps {


handleSort:(field:keyof ResultItem, sortDirection:string)=>void;
field:keyof ResultItem;
pressedSort:keyof ResultItem | null;
}
const SortToggleButton: React.FC<SortToggleButtonProps> = ({handleSort, field, pressedSort}) => {
    const[pressed, setPressed]= useState(false);
  
    const handlePress=(field:keyof ResultItem, direction:string)=>{
        handleSort(field, direction)
        setPressed(!pressed)
        
    }
  let isPressed = pressedSort === field;
    return (
  

                    <div>
                        
                    {isPressed? isPressed && pressed ?<Button className="bg-gray-600" onClick={()=>handlePress(field, "desc")}>⌃</Button>
                    :<Button className="bg-gray-600" onClick={()=>handlePress(field,"asc")}>˅</Button>:<Button className="bg-gray-400" onClick={()=>handlePress(field, "desc")}>⌃</Button>}
                    </div>
    )
};

export default SortToggleButton;
