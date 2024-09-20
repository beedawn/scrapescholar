import React, {useState} from 'react';
import LinePlot from './d3/LinePlot';
import BubblePlot from './d3/BubblePlot';
import { ResultItem } from '../views/SearchView';
import Button from './Button';
interface SearchResultsProps {
    displayInputs: string[];
    results: ResultItem[];
    className?: string;
    emptyString?: string;
    disableD3?: boolean;
    inputs: string[];
    bubbleInputs: { x: number, y: number, radius: number, color: string, label: string }[];
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, displayInputs, className, emptyString, disableD3 = false, inputs, bubbleInputs }) => {
  
   const [selectedArticle, setSelectedArticle] = useState(-1);
  
    return (
        <div className={className}>
            <div className="float-left p-12 max-w-md sm:max-w-screen-xs md:max-w-screen-xs lg:max-w-screen-md xl:max-w-screen-lg">
                {results.length !== 0 && displayInputs[0] !== emptyString ? (
                    <div>
                        <div className="topContainer">
                            <div className="searchName">search name</div>
                            <a href="test link">
                                <div className="downloadButton text-right"><Button>Download</Button></div>
                            
                            </a> 
                            </div>
                        <p>
                            You searched {displayInputs}
                        </p>
                        <div>
                            {disableD3 ? (<></>) : (<>
                                <BubblePlot data={bubbleInputs}></BubblePlot></>)}
                        </div>
                        <div className="overflow-x-auto">
                            <table className=" min-w-full table-auto border-collapse border border-gray-300">
                                <thead>
                                    <tr>
                                        <th className="border border-gray-300">Title</th>
                                        <th className="border border-gray-300">Year</th>
                                        <th className="border border-gray-300">Cited By</th>
                                        <th className="border border-gray-300">URL</th>
                                        <th className="border border-gray-300">Abstract</th>
                                        <th className="border border-gray-300">Document Type</th>
                                        <th className="border border-gray-300">Source</th>
                                        <th className="border border-gray-300">Evaluation Criteria</th>
                                        <th className="border border-gray-300">Color</th>
                                        <th className="border border-gray-300">Methodology</th>
                                        <th className="border border-gray-300">Clarity</th>
                                        <th className="border border-gray-300">Completeness</th>
                                        <th className="border border-gray-300">Transparency</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {results.map((result, index) => (
                                        <tr key={result.id || index} className={` ${selectedArticle === index ? 'bg-blue-500':'hover:bg-gray-500'}`} onClick={()=>{setSelectedArticle(index)}}>
                                            <td className="border border-gray-300"><a href={result.link}>{result.title}</a></td>
                                            <td className="border border-gray-300">{result.date}</td>
                                            <td className="border border-gray-300">{result.citedby}</td>
                                            <td className="border border-gray-300"><a href={result.link}>{result.link}</a></td>
                                            <td className="border border-gray-300"></td>
                                            <td className="border border-gray-300"></td>
                                            <td className="border border-gray-300">{result.source}</td>
                                            <td className="border border-gray-300">accept</td>
                                            <td className="border border-gray-300">
                                                <select className="text-black" >
                                                    <option value="red" className='bg-red-600'>Red</option>
                                                    <option value="yellow" className="bg-yellow">Yellow</option>
                                                    <option className="bg-green" value="green">Green</option>
                                                </select>
                                            </td>
                                            <td className="border border-gray-300">0</td>
                                            <td className="border border-gray-300">0</td>
                                            <td className="border border-gray-300">0</td>
                                            <td className="border border-gray-300">0</td>
                                        </tr>

                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                ) :
                    results.length === 0 && displayInputs[0] === ''
                        ?
                        (<p className="bg-red-800 p-2 rounded">
                            Please enter a keyword
                        </p>)
                        : (results.length === 0 && displayInputs[0] !== '' ? (<p>No Results Found</p>) : (<p>Loading...</p>))}
            </div>
        </div>
    );
};

export default SearchResults;
