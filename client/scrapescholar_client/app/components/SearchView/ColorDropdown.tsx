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
  <div onClick={()=>{setIsOpen(!isOpen)}}  >
      
      {!isOpen&&(<div className={`p-2 flex items-center ${selected.css}`}>{selected.value} <svg className={`m-1 w-2 h-2 rotate-180`}
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"
                                strokeWidth="2" d="M9 5 5 1 1 5" />
                        </svg></div>)}

      <div>
        {isOpen&&(<div className="p-3 bg-slate-800 text-white">   <div>× Close </div>     <div className="p-2 bg-red-600" onClick={()=>setSelected({value:"Not Relevant",css:"bg-red-600"})}>Not Relevant</div>
        <div className="bg-yellow-600 p-2 " onClick={()=>setSelected({value:"SemiRelevant",css:"bg-yellow-600"})}>SemiRelevant</div>
        <div className="bg-green-600 p-2 " onClick={()=>setSelected({value:"Relevant",css:"bg-green-600"})}>Relevant</div>
        
        
        </div>

        )}</div>
    </div>



</>)


  }
  export default ColorDropdown;
