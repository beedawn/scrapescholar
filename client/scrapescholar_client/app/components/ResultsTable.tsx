import React, { useState } from 'react';
import { ResultItem } from '../views/SearchView';
import SortToggleButton from './SortToggleButton';
import DynamicUserField from './DynamicUserField';


export interface EditableCell {
    relevance: boolean;
    methodology: boolean;
    clarity: boolean;
    completeness: boolean;
    transparency: boolean;
    [key: string]: any;
}

interface ResultsTableProps {
    results: ResultItem[];
    setResults: (item: ResultItem[]) => void;
    selectedArticle: number;
    setSelectedArticle: (index: number) => void;
}

export const sortResults = (array: ResultItem[], field: keyof ResultItem, sortDirection: string): ResultItem[] => {

    return array.sort((a,b)=>{
        const aValue = a[field];
        const bValue = b[field];

        if (typeof aValue === "number" && typeof bValue === "number") {
            return sortDirection === "asc" ? aValue - bValue : bValue - aValue;
        }
        if (typeof aValue === "string" && typeof bValue === "string") {
            return sortDirection === "asc" ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
        }
        if (typeof aValue === "number") {
            // Numbers come before strings
            return sortDirection === "asc" ? -1 : 1;
        }
        if (typeof bValue === "number") {
            // Strings come after numbers
            return sortDirection === "asc" ? 1 : -1; 
        }
        return 0; 
})
 };

const ResultsTable: React.FC<ResultsTableProps> = ({ results, selectedArticle, setSelectedArticle, setResults }) => {
    const [editableResults, setEditableResults] = useState<ResultItem[]>([...results]);
    const handleSort = (field: keyof ResultItem, sortDirection: string) => {
        const sortedResults = sortResults([...results], field, sortDirection);
        setPressedSort(field);
        const orderedEditableResults = sortedResults.map(result => {
            // Find the corresponding item in 'editableResults' by matching the 'id'
            return editableResults.find(editable => editable.id === result.id) || result;
        });
        setEditableResults(orderedEditableResults);
        setResults(sortedResults);
    }
    const [pressedSort, setPressedSort] = useState<keyof ResultItem | null>(null);
    const [editableCells, setEditableCells] = useState<EditableCell[]>(results.map((result) => ({
        id:result.id,
        relevance: false, methodology: false, clarity: false, completeness: false, transparency: false
    })));

    const handleCellClick = (index: number, field: keyof EditableCell) => {
        const updatedCells: EditableCell[] = [...editableCells];
        updatedCells[index][field as keyof EditableCell] = !updatedCells[index][field as keyof EditableCell];
        setEditableCells(updatedCells)
    }
    const handleFieldChange = (id: number, field: keyof EditableCell, value: string) => {
        const updatedResults = editableResults.map(result => 
            result.id === id ? { ...result, [field]: value } : result
        );
        setEditableResults(updatedResults);
    }
    const handleFieldConfirm = async () => {
        setResults(editableResults);
        //send request to backend to update value?
    }
    return (
        <div className="overflow-x-auto">
            <table className=" min-w-full table-auto border-collapse border border-gray-300">
                <thead>
                    <tr>
                        <th className="border border-gray-300">
                            Title
                            <SortToggleButton handleSort={handleSort} field="title" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Year
                            <SortToggleButton handleSort={handleSort} field="date" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Cited By
                            <SortToggleButton handleSort={handleSort} field="citedby" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            URL
                            <SortToggleButton handleSort={handleSort} field="link" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Abstract
                            <SortToggleButton handleSort={handleSort} field="abstract" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Document Type
                            <SortToggleButton handleSort={handleSort} field="document_type" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Source
                            <SortToggleButton handleSort={handleSort} field="source" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Evaluation Criteria
                            <SortToggleButton handleSort={handleSort} field="evaluation_criteria" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Assessment
                            <SortToggleButton handleSort={handleSort} field="color" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Relevance Score
                            <SortToggleButton handleSort={handleSort} field="relevance_score" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Methodology
                            <SortToggleButton handleSort={handleSort} field="methodology" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Clarity
                            <SortToggleButton handleSort={handleSort} field="clarity" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Completeness
                            <SortToggleButton handleSort={handleSort} field="completeness" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Transparency
                            <SortToggleButton handleSort={handleSort} field="transparency" pressedSort={pressedSort} />
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((result, index) => (
                        <tr key={result.id} className={` ${selectedArticle === result.id ? 'bg-blue-500' : 'hover:bg-gray-500'}`}
                            onClick={() => { setSelectedArticle(result.id) }} data-testid='row'>
                            <td className="border border-gray-300" ><a href={result.link}>{result.title}</a></td>
                            <td className="border border-gray-300" >{result.date}</td>
                            <td className="border border-gray-300" >{result.citedby}</td>
                            <td className="border border-gray-300" ><a href={result.link}>{result.link}</a></td>
                            <td className="border border-gray-300" >{result.abstract}</td>
                            <td className="border border-gray-300" >{result.document_type}</td>
                            <td className="border border-gray-300" >{result.source}</td>
                            <td className="border border-gray-300" >{result.evaluation_criteria}</td>
                            <td className="border border-gray-300" >
                                {result.color}
                                <select className="text-black" >
                                    <option value="red" className='bg-red-600'>Red</option>
                                    <option value="yellow" className="bg-yellow">Yellow</option>
                                    <option className="bg-green" value="green">Green</option>
                                </select>
                            </td>
                            <td className="border border-gray-300" >{result.relevance_score}%</td>
                            <td className="border border-gray-300" >
                                <DynamicUserField editableResults={editableResults}
                                    field="methodology" handleFieldConfirm={handleFieldConfirm}
                                    handleCellClick={handleCellClick} result={result} editableCells={editableCells}
                                    handleFieldChange={handleFieldChange} index={index}/>
                            </td>
                            <td className="border border-gray-300" >
                                <DynamicUserField editableResults={editableResults}
                                    field="clarity" handleFieldConfirm={handleFieldConfirm}
                                    handleCellClick={handleCellClick} result={result}
                                    editableCells={editableCells} handleFieldChange={handleFieldChange} index={index} />
                            </td>
                            <td className="border border-gray-300">
                                <DynamicUserField editableResults={editableResults}
                                    field="completeness" handleFieldConfirm={handleFieldConfirm}
                                    handleCellClick={handleCellClick} result={result}
                                    editableCells={editableCells} handleFieldChange={handleFieldChange} index={index} />
                            </td>
                            <td className="border border-gray-300" >
                                <DynamicUserField editableResults={editableResults}
                                    field="transparency" handleFieldConfirm={handleFieldConfirm}
                                    handleCellClick={handleCellClick} result={result}
                                    editableCells={editableCells}
                                    handleFieldChange={handleFieldChange} index={index}/>
                            </td>
                        </tr>

                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ResultsTable;