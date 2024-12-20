import React, { useState, useEffect, useRef } from 'react';
import { ResultItem } from '../../views/SearchView';
import SortToggleButton from './SortToggleButton';
import DynamicUserField from './DynamicUserField';
import ColorDropdown from './ColorDropdown';
import EvaluationCriteriaDropdown from './EvaluationCriteriaDropdown';
import apiCalls from '@/app/api/apiCalls';
import Button from '../Button';
import AbstractModal from './modal/AbstractModal';
import DOMPurify from 'dompurify';
import DeleteArticleModal from './modal/DeleteArticle';

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
    onArticleClick: (articleId: number) => void;
    setRelevanceChanged: (item: boolean) => void;
    relevanceChanged: boolean;
    handlePastSearchSelectionSearchID:
    (search_id: number) => void;
    currentSearchID: number;
    isMobile: boolean;
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
    onArticleClick,
    setRelevanceChanged, relevanceChanged,
    handlePastSearchSelectionSearchID, currentSearchID,
    isMobile
}) => {
    const containerRef = useRef<HTMLDivElement>(null);
    let scrollBy = 350;
    if (isMobile) {
        scrollBy = 200;
    }
    const scrollLeft = () => {
        if (containerRef.current) {
            containerRef.current.scrollBy({
                left: scrollBy * -1,
                behavior: 'smooth',
            });
        }
    };

    const scrollRight = () => {
        if (containerRef.current) {
            containerRef.current.scrollBy({
                left: scrollBy,
                behavior: 'smooth',
            });
        }
    };

    const [editableResults, setEditableResults]
        = useState<ResultItem[]>([...results]);
    const [isAdminUser, setIsAdminUser] = useState<boolean>(false);
    const [abstractText, setAbstractText] = useState<string>("");
    const handleSort = (field: keyof ResultItem, sortDirection: string) => {
        const sortedResults = sortResults([...results], field, sortDirection);
        setPressedSort(field);
        const orderedEditableResults = sortedResults.map(result => {
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
            if (!isAdmin) {
                console.warn("Only Professors can edit fields.");
                return;
            }
            targetCell[field as keyof EditableCell] = !targetCell[field as keyof EditableCell];
            setEditableCells(updatedCells);
        } else {
            console.error(`No editable cell found with article_id ${article_id}`);
        }
    };

    useEffect(() => {
        const findAdmin = async () => {
            try {
                const result = await isAdmin();
                setIsAdminUser(result === "true");
            } catch (error) {
                console.error("Failed to check admin status:", error);
            }
        };
        findAdmin();
    }, []);
    const handleFieldChange = (id: number, field: keyof EditableCell, value: string) => {
        const sanitizedValue = DOMPurify.sanitize(value);
        const updatedResults = editableResults.map(result =>
            result.article_id === id ? { ...result, [field]: sanitizedValue } : result
        );
        setEditableResults(updatedResults);
    }
    const { putUserData, isAdmin } = apiCalls();
    const handleFieldConfirm = async () => {
        setResults(editableResults);
        for (let item of editableResults) {
            const putrequest = {
                "article_id": item.article_id,
                "methodology": item.methodology.toString(),
                "clarity": item.clarity.toString(),
                "transparency": item.transparency.toString(),
                "completeness": item.completeness.toString()
            }
            await putUserData(putrequest)
        }
    }
    const [deleteArticleModalActive, setDeleteArticleModalActive] = useState<boolean>(false)
    const [articleToDelete, setArticleToDelete] = useState<ResultItem>();
    const openDeleteArticleModal = (article: ResultItem) => {
        setDeleteArticleModalActive(true);
        setArticleToDelete(article)
    }
    return (
        <>
            {deleteArticleModalActive && articleToDelete !== undefined ?
                <DeleteArticleModal
                    handlePastSearchSelectionSearchID={handlePastSearchSelectionSearchID}
                    setDeleteArticleModalActive={setDeleteArticleModalActive}
                    currentSearchID={currentSearchID}
                    articleToDelete={articleToDelete} />
                :
                <></>}
            {(abstractText.length > 0) ? (<AbstractModal setAbstractText={setAbstractText} text={abstractText} />) : <></>}
            <button className="absolute bottom-1 bg-emerald-500 text-black px-5 py-1" onClick={scrollLeft} data-testid="scroll_left">
                ˂
            </button>
            <button className="absolute bottom-1 right-10 bg-emerald-500 text-black px-5 py-1" onClick={scrollRight} data-testid="scroll_right">
                ˃
            </button>
            <div className="overflow-x-auto" ref={containerRef}>
                <table className=" min-w-full table-auto border-collapse border border-gray-500">
                    <thead>
                        <tr>
                            <th className="border border-gray-500">
                                {/* delete header spacer */}
                            </th>
                            <th className="border border-gray-500">
                                Title
                                <SortToggleButton handleSort={handleSort}
                                    field="title" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Date
                                <SortToggleButton handleSort={handleSort}
                                    field="date" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Cited By
                                <SortToggleButton handleSort={handleSort}
                                    field="citedby" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                URL
                                <SortToggleButton handleSort={handleSort}
                                    field="link" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Abstract
                                <SortToggleButton handleSort={handleSort}
                                    field="abstract" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Document Type
                                <SortToggleButton handleSort={handleSort}
                                    field="document_type" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Source
                                <SortToggleButton handleSort={handleSort}
                                    field="source" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Evaluation Criteria
                                <SortToggleButton handleSort={handleSort}
                                    field="evaluation_criteria" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Assessment
                                <SortToggleButton handleSort={handleSort}
                                    field="color" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Relevance Score
                                <SortToggleButton handleSort={handleSort}
                                    field="relevance_score" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Methodology
                                <SortToggleButton handleSort={handleSort}
                                    field="methodology" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Clarity
                                <SortToggleButton handleSort={handleSort}
                                    field="clarity" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Completeness
                                <SortToggleButton handleSort={handleSort}
                                    field="completeness" pressedSort={pressedSort} />
                            </th>
                            <th className="border border-gray-500">
                                Transparency
                                <SortToggleButton handleSort={handleSort}
                                    field="transparency" pressedSort={pressedSort} />
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {results.map((result, index) => (
                            <tr key={result.article_id} className=
                                {` ${selectedArticle === result.article_id ? 'bg-blue-500' : 'hover:bg-gray-400'}`}
                                onClick={() => {
                                    setSelectedArticle(result.article_id);
                                    onArticleClick(result.article_id); // Call onArticleClick when an article is clicked
                                }} data-testid='row'>
                                <td className="border border-gray-500" >
                                    <button className="bg-red-600 text-2xl p-1 m-2 rounded text-white"
                                        onClick={() => {
                                            openDeleteArticleModal(result)
                                        }} data-testid="delete_article_button">
                                        ␡
                                    </button>
                                </td>
                                <td className="border border-gray-500" >
                                    <a href={result.link}>
                                        {result.title}
                                    </a>
                                </td>
                                <td className="border border-gray-500" >{result.date}</td>
                                <td className="border border-gray-500" >{result.citedby}</td>
                                <td className="border border-gray-500" >
                                {result.link=="http://null"?<>Potentially malicious link detected. Blocked for user safety.</>:<a href={result.link}>
                                        {result.link}
                                    </a>}
                                    
                                </td>
                                <td className="border border-gray-500">
                                    {result.abstract != null && result.abstract.length > 0 ? (
                                        <>
                                            {result.abstract.slice(0, 200)}...
                                            <div>
                                                <Button onClick={() => { setAbstractText(result.abstract) }}>Expand</Button>
                                            </div>
                                        </>
                                    ) : (
                                        <></>
                                    )}
                                </td>
                                <td className="border border-gray-500" >{result.document_type}</td>
                                <td className="border border-gray-500" >{result.source}</td>
                                <td className="border border-gray-500" >
                                    <EvaluationCriteriaDropdown article_id={result.article_id}
                                        evaluationValue={result.evaluation_criteria}
                                        disabled={!isAdminUser} />
                                </td>
                                <td className="border border-gray-500" >
                                    <ColorDropdown article_id={result.article_id}
                                        colorValue={result.color}
                                        setRelevanceChanged={setRelevanceChanged}
                                        relevanceChanged={relevanceChanged} />
                                </td>
                                <td className="border border-gray-500" >{result.relevance_score}%</td>
                                <td className="border border-gray-500" >
                                    <DynamicUserField editableResults={editableResults}
                                        field="methodology" handleFieldConfirm={handleFieldConfirm}
                                        handleCellClick={handleCellClick} result={result} editableCells={editableCells}
                                        handleFieldChange={handleFieldChange} index={index} />
                                </td>
                                <td className="border border-gray-500" >
                                    <DynamicUserField editableResults={editableResults}
                                        field="clarity" handleFieldConfirm={handleFieldConfirm}
                                        handleCellClick={handleCellClick} result={result}
                                        editableCells={editableCells} handleFieldChange={handleFieldChange} index={index} />
                                </td>
                                <td className="border border-gray-500">
                                    <DynamicUserField editableResults={editableResults}
                                        field="completeness" handleFieldConfirm={handleFieldConfirm}
                                        handleCellClick={handleCellClick} result={result}
                                        editableCells={editableCells} handleFieldChange={handleFieldChange} index={index} />
                                </td>
                                <td className="border border-gray-500" >
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
