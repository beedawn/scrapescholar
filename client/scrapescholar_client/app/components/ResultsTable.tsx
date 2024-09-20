import React, {useState} from 'react';
import { ResultItem } from '../views/SearchView';
import SortToggleButton from './SortToggleButton';

interface ResultsTableProps {
    results: ResultItem[];
    setResults: (item: ResultItem[]) => void;
    selectedArticle: number;
    setSelectedArticle: (index: number) => void;
}

const ResultsTable: React.FC<ResultsTableProps> = ({ results, selectedArticle, setSelectedArticle, setResults }) => {
    const sortResults = (array: ResultItem[], field: keyof ResultItem, sortDirection: string): ResultItem[] => {
        if (sortDirection === "asc")
            return array.sort((a, b) => {
                if (a[field] < b[field]) return -1;
                if (a[field] > b[field]) return 1;
                return 0;
            });
        else
            return array.sort((a, b) => {
                if (a[field] > b[field]) return -1;
                if (a[field] < b[field]) return 1;
                return 0;
            });
    };
    const handleSort = (field: keyof ResultItem, sortDirection: string) => {
        const sortedResults = sortResults([...results], field, sortDirection);
        console.log(sortedResults)
        setPressedSort(field);
        setResults(sortedResults)
    }
    const [pressedSort, setPressedSort]=useState<keyof ResultItem | null>(null);
    return (

        <div className="overflow-x-auto">

            <table className=" min-w-full table-auto border-collapse border border-gray-300">
                <thead>
                    <tr>
                        <th className="border border-gray-300">Title<SortToggleButton handleSort={handleSort} field="title" pressedSort={pressedSort} /></th>
                        <th className="border border-gray-300">Year<SortToggleButton handleSort={handleSort} field="date" pressedSort={pressedSort}/></th>
                        <th className="border border-gray-300">Cited By<SortToggleButton handleSort={handleSort} field="citedby" pressedSort={pressedSort}/></th>
                        <th className="border border-gray-300">URL</th>
                        <th className="border border-gray-300">Abstract</th>
                        <th className="border border-gray-300">Document Type</th>
                        <th className="border border-gray-300">Source<SortToggleButton handleSort={handleSort} field="source" pressedSort={pressedSort}/></th>
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
                        <tr key={result.id} className={` ${selectedArticle === index ? 'bg-blue-500' : 'hover:bg-gray-500'}`} onClick={() => { setSelectedArticle(index) }}>
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
