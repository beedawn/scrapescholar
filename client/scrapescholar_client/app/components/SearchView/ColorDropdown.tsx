import React, { useState } from 'react';



interface ColorDropdownProps {
    // value: string;
    // onDropdownChange: (e: React.ChangeEvent<HTMLSelectElement>) => void;
    // className?: string;
    // valueArray: any[];
    key:number;
  }
  const ColorDropdown: React.FC<ColorDropdownProps> = (key) => {
    const [selected, setSelected] = useState({value:"Relevancy",css:"bg-white-600"});
    const [isOpen, setIsOpen]=useState(false);


  


return(<>
  <div onClick={()=>{setIsOpen(!isOpen)}} >
      
      <div className={selected.css}>{selected.value}</div>

      <div>
        {isOpen&&(<>        <div className="bg-red-600" onClick={()=>setSelected({value:"Not Relevant",css:"bg-red-600"})}>Not Relevant</div>
        <div className="bg-yellow-600" onClick={()=>setSelected({value:"SemiRelevant",css:"bg-yellow-600"})}>SemiRelevant</div>
        <div className="bg-green-600" onClick={()=>setSelected({value:"Relevant",css:"bg-green-600"})}>Relevant</div>
        
        
        </>

        )}</div>
    </div>



</>)


  }
  export default ColorDropdown;
