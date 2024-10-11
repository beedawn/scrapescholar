import React, { ChangeEvent, useEffect, useState } from 'react';
import { ResultItem } from '../../views/SearchView';
import { EditableCell } from './ResultsTable';

import {apiCalls} from '../apiCalls';
import { ApiError } from 'next/dist/server/api-utils';
type EditableField =
    'relevance' | 'methodology' | 'clarity'
    | 'completeness' | 'transparency';

interface DynamicUserFieldProps {
    field: EditableField;
    handleCellClick: (index: number, field: EditableField) => void;
    editableCells: EditableCell[];
    result: ResultItem;
    handleFieldChange: (index: number, field: keyof EditableCell,
        value: string) => void;
    handleFieldConfirm: () => void;
    editableResults: ResultItem[];
    index: number;
}

const DynamicUserField: React.FC<DynamicUserFieldProps> =
    ({ field, handleCellClick, result, editableCells,
        handleFieldChange, handleFieldConfirm, editableResults, index }) => {
        const [currentCell, setCurrentCell]=useState<EditableCell>();
        useEffect(()=>{
        const currentCell = editableCells.find((cell) => {
            return cell.article_id == result.article_id
        })
        setCurrentCell(currentCell)
        console.log(currentResult)
        console.log(currentResult?.[field])
    },[editableCells])
    const currentResult = editableResults.find((cell) => {
        return cell.article_id == result.article_id
    })
        
        return (
            <>
                {currentCell?.[field] ?
                    (<><form onSubmit={async (e) => {
                        e.preventDefault();
                        await handleFieldConfirm();
                        handleCellClick(result.article_id, field)
                    }}>
                        <input style={{ color: "black", width: "75%" }}
                            value={currentResult ? currentResult[field] : ''}
                            onChange={(e: ChangeEvent<HTMLInputElement>) => {
                                handleFieldChange(result.article_id, field, e.target.value)
                            }
                            }
                        />
                        <button style={{ display: "inline", margin: "5px" }}
                            type="button"
                            onClick={() => {
                                handleCellClick(result.article_id, field)
                            }
                            }
                        >
                            ×
                        </button>
                        <button style={{ display: "inline", margin: "5px" }}
                            type="submit"

                        >
                            ✔
                        </button>
                    </form>
                    </>)
                    :
                    (<>
                        {result[field]}
                        <button style={{ display: "inline" }}
                            onClick={() => { handleCellClick(result.article_id, field) }}>
                            ✎
                        </button>
                    </>
                    )
                }
            </>)
    };

export default DynamicUserField;
