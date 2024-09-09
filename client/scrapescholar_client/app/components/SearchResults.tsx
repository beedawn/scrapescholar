import React from 'react';
import LinePlot from './d3/LinePlot';
import BubblePlot from './d3/BubblePlot';
import { ResultItem } from '../views/SearchView';
interface SearchResultsProps {
    displayInputs: string[];
    results: ResultItem[];
    className?: string;
    emptyString?: string;
    disableD3?:boolean;
    inputs:string[];
}

const SearchResults: React.FC<SearchResultsProps> = ({results, displayInputs, className, emptyString, disableD3=false, inputs }) => {
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
                {results.length !== 0 && displayInputs[0] !== emptyString ? (
                     <div>
                     <p>
                         You searched {displayInputs}
                     </p>
                  
                    <div>

                        {disableD3?(<></>):(<><LinePlot data={[20, 40, 50, 60]} width={200} height={200} /> <BubblePlot data={bubbleInputs}></BubblePlot></>)}

                    </div>

                    <div>
                    <ul>
      {results.map((result) => (
        <>
        <li><a href={result.link}>{result.title}</a></li>
    
        </>
      ))}
    </ul>
                     </div>
                    </div>
                ) : (
                    results.length !== 0
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
