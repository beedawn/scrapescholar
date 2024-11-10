import React, { useState, useEffect } from 'react';
import apiCalls from '@/app/api/apiCalls';

import Relevance from '@/app/types/Relevance';
interface ColorDropdownProps {
   //need some kind of state here to trigger graph updates
    colorValue:string;
    article_id:number;
    setRelevanceChanged: (item: boolean) => void;
    relevanceChanged:boolean;
  }
  const ColorDropdown: React.FC<ColorDropdownProps> = ({article_id,colorValue, setRelevanceChanged, relevanceChanged}) => {
    const [selected, setSelected] = useState({value:"Relevancy",css:"bg-white-600"});
    const [isOpen, setIsOpen]=useState(false);
    useEffect(()=>{

      if(colorValue=="Relevant")
        handleChange(Relevance.Relevant)
      if(colorValue=="SemiRelevant")
        handleChange(Relevance.SemiRelevant)
      if(colorValue=="Not Relevant")
        handleChange(Relevance.NotRelevant)

      
    },[])
    const {putUserData}=apiCalls();
  const handleChange= async(input:Relevance)=>{
    let selectedValue='';
    let cssStyling='';
    switch(input){
      case(Relevance.NotRelevant):
        selectedValue="Not Relevant";
        cssStyling="bg-red-600";
        
        break;
      case(Relevance.SemiRelevant):
        selectedValue="SemiRelevant";
        cssStyling="bg-yellow-600";
        break;
      case(Relevance.Relevant):
        selectedValue="Relevant";
        cssStyling="bg-green-600";
        break;
      default:
        break;

    }
    setSelected({value:selectedValue,css:cssStyling});
  const putRequest ={
    "article_id":article_id,
    "relevancy_color":selectedValue

  }
  setRelevanceChanged(!relevanceChanged)
  await putUserData(putRequest)

  }

return(<>
  <div onClick={()=>{setIsOpen(!isOpen)}} data-testid="relevancy-column-default" >
      
      {!isOpen&&(<div className={`p-2 flex items-center ${selected.css}`} >{selected.value} <svg className={`m-1 w-2 h-2 rotate-180`}
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"
                                strokeWidth="2" d="M9 5 5 1 1 5" />
                        </svg></div>)}

      <div>
        {isOpen&&(
          <div className="p-3 bg-slate-800 text-white">   
          <div>
            × Close 
          </div>     
          <div className="p-2 bg-red-600" onClick={()=>handleChange(Relevance.NotRelevant)}>
            Not Relevant
          </div>
        <div className="bg-yellow-600 p-2 " onClick={()=>handleChange(Relevance.SemiRelevant)}>
          SemiRelevant
        </div>
        <div className="bg-green-600 p-2 " onClick={()=>handleChange(Relevance.Relevant)}>
          Relevant
        </div>
        
        
        </div>

        )}</div>
    </div>



</>)


  }
  export default ColorDropdown;
