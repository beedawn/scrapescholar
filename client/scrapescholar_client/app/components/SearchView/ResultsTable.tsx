import React, { useState, useEffect } from 'react';
import { ResultItem } from '../../views/SearchView';
import SortToggleButton from './SortToggleButton';
import DynamicUserField from './DynamicUserField';
import ColorDropdown from './ColorDropdown';
import EvaluationCriteriaDropdown from './EvaluationCriteriaDropdown';
import apiCalls from '@/app/api/apiCalls';
import Button from '../Button';
import AbstractModal from './modal/AbstractModal';

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
    selectedArticle: number | null; // Updated to allow null
    setSelectedArticle: (index: number | null) => void;  // Allow null
    setLoading:(state:boolean)=> void;
    onArticleClick: (articleId: number) => void;
    setRelevanceChanged: (item: boolean) => void;
    relevanceChanged:boolean;
}


export const sortResults = (array: ResultItem[],
    field: keyof ResultItem,
    sortDirection: string): ResultItem[] => {
    return [...array].sort((a, b) => {
        const aValue = a[field];
        const bValue = b[field];
        if (typeof aValue === "number" && typeof bValue === "number") {
            return sortDirection === "asc" ? aValue - bValue : bValue - aValue;
        }
        if (typeof aValue === "string" && typeof bValue === "string") {
            return sortDirection === "asc" ? aValue.localeCompare(bValue) :
                bValue.localeCompare(aValue);
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

const ResultsTable: React.FC<ResultsTableProps> = ({
    results, selectedArticle, setSelectedArticle, setResults, 
    setLoading, onArticleClick, setRelevanceChanged, relevanceChanged
}) => {
    const [editableResults, setEditableResults]
        = useState<ResultItem[]>([...results]);
    const [isAdminUser, setIsAdminUser] = useState<boolean>(false);
    const [abstractText,setAbstractText]=useState<string>("");
    const handleSort = (field: keyof ResultItem, sortDirection: string) => {
        const sortedResults = sortResults([...results], field, sortDirection);
        setPressedSort(field);
        const orderedEditableResults = sortedResults.map(result => {
            // Find the corresponding item in 'editableResults' by matching the 'id'
            return editableResults.find(editable =>
                editable.article_id === result.article_id) || result;
        });
        setEditableResults(orderedEditableResults);
        setResults(sortedResults);
    }
    const [pressedSort, setPressedSort] = useState<keyof ResultItem | null>(null);
    const [editableCells, setEditableCells] = useState<EditableCell[]>
        (results.map((result) => ({
            article_id: result.article_id,
            relevance: false,
            methodology: false,
            clarity: false,
            completeness: false,
            transparency: false
        })));

        const handleCellClick = (article_id: number, field: keyof EditableCell) => {
            const updatedCells: EditableCell[] = [...editableCells];
        
            const targetCell = updatedCells.find(cell => cell.article_id === article_id);
        
            if (targetCell) {
                // Allow edit toggling only if the user is a Professor
                if (!isAdmin) {
                    console.warn("Only Professors can edit fields.");
                    return;
                }
        
                // Toggle the field's editable state
                targetCell[field as keyof EditableCell] = !targetCell[field as keyof EditableCell];
        
                // Update the state with the modified cells array
                setEditableCells(updatedCells);
            } else {
                console.error(`No editable cell found with article_id ${article_id}`);
            }
        };
    
    useEffect(() => {
        const findAdmin = async () => {
            try {
                const result = await isAdmin();
                console.log("Admin status:", result); // Log admin status
                setIsAdminUser(result === "true");
            } catch (error) {
                console.error("Failed to check admin status:", error);
            }
        };
        findAdmin();
    }, []);   
    const handleFieldChange = (id: number, field: keyof EditableCell, value: string) => {
        const updatedResults = editableResults.map(result =>
            result.article_id === id ? { ...result, [field]: value } : result
        );

        setEditableResults(updatedResults);
    }
    const {putUserData, isAdmin}=apiCalls();
    const handleFieldConfirm = async () => {
        setResults(editableResults);
        console.log("editable results")
        console.log(editableResults)
        for (let item of editableResults){
            const putrequest={
                "article_id":item.article_id,
                "methodology":item.methodology.toString(),
                "clarity":item.clarity.toString(),
                "transparency":item.transparency.toString(),
                "completeness":item.completeness.toString()

            }
            
            await putUserData(putrequest)
        }
        //send request to backend to update value?
    }


    return (
        <>
        {(abstractText.length>0)?(<AbstractModal setAbstractText={setAbstractText} text={abstractText}/>):<></>}
        <div className="overflow-x-auto">
            <table className=" min-w-full table-auto border-collapse border border-gray-300">
                <thead>
                    <tr>
                        <th className="border border-gray-300">
                            Title
                            <SortToggleButton handleSort={handleSort}
                                field="title" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Year
                            <SortToggleButton handleSort={handleSort}
                                field="date" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Cited By
                            <SortToggleButton handleSort={handleSort}
                                field="citedby" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            URL
                            <SortToggleButton handleSort={handleSort}
                                field="link" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Abstract
                            <SortToggleButton handleSort={handleSort}
                                field="abstract" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Document Type
                            <SortToggleButton handleSort={handleSort}
                                field="document_type" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Source
                            <SortToggleButton handleSort={handleSort}
                                field="source" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Evaluation Criteria
                            <SortToggleButton handleSort={handleSort}
                                field="evaluation_criteria" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Assessment
                            <SortToggleButton handleSort={handleSort}
                                field="color" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Relevance Score
                            <SortToggleButton handleSort={handleSort}
                                field="relevance_score" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Methodology
                            <SortToggleButton handleSort={handleSort}
                                field="methodology" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Clarity
                            <SortToggleButton handleSort={handleSort}
                                field="clarity" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Completeness
                            <SortToggleButton handleSort={handleSort}
                                field="completeness" pressedSort={pressedSort} />
                        </th>
                        <th className="border border-gray-300">
                            Transparency
                            <SortToggleButton handleSort={handleSort}
                                field="transparency" pressedSort={pressedSort} />
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((result, index) => (
                        <tr key={result.article_id} className=
                            {` ${selectedArticle === result.article_id ? 'bg-blue-500' : 'hover:bg-gray-500'}`}
                            onClick={() => { 
                                setSelectedArticle(result.article_id);
                                onArticleClick(result.article_id); // Call onArticleClick when an article is clicked
                            }} data-testid='row'>
                            <td className="border border-gray-300" >
                                <a href={result.link}>
                                    {result.title}
                                </a>
                            </td>
                            <td className="border border-gray-300" >{result.date}</td>
                            <td className="border border-gray-300" >{result.citedby}</td>
                            <td className="border border-gray-300" >
                                <a href={result.link}>
                                    {result.link}
                                </a>
                            </td>
                            <td className="border border-gray-300">
  {result.abstract.length > 0 ? (
    <>
      {result.abstract.slice(0, 200)}...
      <div>
        <Button onClick={()=>{setAbstractText(result.abstract)}}>Expand</Button>
      </div>
    </>
  ) : (
    <></>
  )}
</td>
                            <td className="border border-gray-300" >{result.document_type}</td>
                            <td className="border border-gray-300" >{result.source}</td>
                            <td className="border border-gray-300" >
                            <EvaluationCriteriaDropdown article_id={result.article_id} evaluationValue={result.evaluation_criteria} disabled={!isAdminUser} />



                            </td>
                            <td className="border border-gray-300" >
                                <ColorDropdown article_id={result.article_id} colorValue={result.color} setRelevanceChanged={setRelevanceChanged} relevanceChanged={relevanceChanged}/>
                            </td>
                            <td className="border border-gray-300" >{result.relevance_score}%</td>
                            <td className="border border-gray-300" >
                                <DynamicUserField editableResults={editableResults}
                                    field="methodology" handleFieldConfirm={handleFieldConfirm}
                                    handleCellClick={handleCellClick} result={result} editableCells={editableCells}
                                    handleFieldChange={handleFieldChange} index={index} />
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
                                    handleFieldChange={handleFieldChange} index={index} />
                            </td>
                        </tr>

                    ))}
                </tbody>
            </table>
        </div>
        </>
    );
};

export default ResultsTable;
