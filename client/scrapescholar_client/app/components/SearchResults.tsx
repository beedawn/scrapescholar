import React from 'react';
import LinePlot from './d3/LinePlot';
import BubblePlot from './d3/BubblePlot';
interface SearchResultsProps {
    displayInputs: string[];
    results: string;
    className?: string;
    emptyString?: string;
    disableD3?:boolean;
    inputs:string[];
}

const SearchResults: React.FC<SearchResultsProps> = ({ children, results, displayInputs, onClick, className, emptyString, disableD3=false, inputs }) => {
   let bubbleInputs = [{x:0, y:0, radius:0, color:"", label:""}];
   if(displayInputs[0]!==undefined){
    const filteredInputs = displayInputs[0].split(' ');
   const filteredInputsAND = filteredInputs.filter((item)=>{
    return item !== "AND"
   })

   const filteredInputsOR = filteredInputsAND.filter((item)=>{
    return item !== "OR"
   })

   const filteredInputsNOT = filteredInputsOR.filter((item)=>{
    return item !== "NOT"
   })
   bubbleInputs=filteredInputsNOT.map((input, i)=>({
    x: i, 
    y: 50, 
    radius:50, 
    color: "green", 
    label:input
   })); 
}


    return (
        <div className={className}>
            <div className="float-left p-12 max-w-fit">
                {results !== emptyString && displayInputs[0] !== emptyString ? (
                     <div>
                     <p>
                         You searched {displayInputs}
                     </p>
                     <div>
                         {results}
                     </div>
                    <div>

                        {disableD3?(<></>):(<><LinePlot data={[20, 40, 50, 60]} width={200} height={200} /> <BubblePlot data={bubbleInputs}></BubblePlot></>)}

                    </div>
                    </div>
                ) : (
                    results !== emptyString
                    &&
                    <p className="bg-red-800 p-2 rounded">
                        Please enter a keyword
                    </p>
                )}
            </div>
        </div>
    );
};

export default SearchResults;
