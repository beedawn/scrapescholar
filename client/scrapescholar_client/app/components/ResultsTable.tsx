import React from 'react';
import { ResultItem } from '../views/SearchView';

interface ResultsTableProps {
    results: ResultItem[];
    setResults: (item:ResultItem[])=>void;
    selectedArticle: number;
    setSelectedArticle: (index: number) => void;
}

const ResultsTable: React.FC<ResultsTableProps> = ({ results, selectedArticle, setSelectedArticle, setResults }) => {


const sort = (array: ResultItem[], field: keyof ResultItem ):ResultItem[] => {

    const newArray=[...array]
    return newArray.sort((a, b) => {
     if (a[field] < b[field]) return -1;
     if (a[field] > b[field]) return 1;
     return 0; 
   });
  
 };
const handleSort = (field: keyof ResultItem)=>{
const sortedResults = sort([...results],field);
setResults(sortedResults)

}
    return (
                        <div className="overflow-x-auto">
                            <button onClick={()=>{handleSort("title")}} >button</button>
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
    );
};

export default ResultsTable;
