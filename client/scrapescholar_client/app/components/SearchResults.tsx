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
   if(inputs!==undefined){
    

   bubbleInputs=inputs.map((input, i)=>({
    x: i, 
    y: 50, 
    radius:50, 
    color: "green", 
    label:input
   })); 
}


    return (
        <div className={className}>
            <div className="float-left p-12 max-w-md max-w-screen-sm">
                {results.length !== 0 && displayInputs[0] !== emptyString ? (
                     <div>
                     <p>
                         You searched {displayInputs}
                     </p>
                  
                    <div>

                        {disableD3?(<></>):(<>
                        
                        <BubblePlot data={bubbleInputs}></BubblePlot></>)}

                    </div>

                    <div>

                    <table>
  <tr>
    <th>Title</th>
    <th>Year</th>
    <th>Cited By</th>
    <th>URL</th>
    <th>Abstract</th>
    <th>Document Type</th>
    <th>Source</th>
    <th>Evaluation Criteria</th>
    <th>Color</th>
        <th>Methodology</th> 	
        <th>Clarity</th>
        <th>Completeness</th>	
        <th>Transparency</th>
  </tr>

  {results.map((result) => (
       <tr key={result.id}>
        <td><a href={result.link}>{result.title}</a></td>
        <td>{result.date}</td>
       <td>#</td>
       <td><a href={result.link}>{result.link}</a></td>
       <td></td>
       <td></td>
       <td>{result.source}</td>
       <td>accept</td>
       <td>
        <select className="text-black" >
        <option value="red" className='bg-red-600'>Red</option>
        <option value="yellow" className="bg-yellow">Yellow</option>
        <option className="bg-green" value="green">Green</option>
        </select>
        </td>
       <td>0</td>
       <td>0</td>
       <td>0</td>
       <td>0</td>
        </tr> 
      
     ))}
</table>

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
