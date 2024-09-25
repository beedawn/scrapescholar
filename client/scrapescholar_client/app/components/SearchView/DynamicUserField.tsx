import React, { ChangeEvent, useState } from 'react';
import { ResultItem } from '../../views/SearchView';
import { EditableCell } from './ResultsTable';
type EditableField = 'relevance' | 'methodology' | 'clarity' | 'completeness' | 'transparency';

interface DynamicUserFieldProps {
    field: EditableField;
    handleCellClick: (index: number, field: EditableField) => void;
    editableCells: EditableCell[];
    result: ResultItem;
    handleFieldChange: (index: number, field: keyof EditableCell, value: string) => void;
    handleFieldConfirm: () => void;
    editableResults: ResultItem[];
    index:number;
}


const DynamicUserField: React.FC<DynamicUserFieldProps> =
    ({ field, handleCellClick, result, editableCells,
        handleFieldChange, handleFieldConfirm, editableResults, index }) => {

const currentResult=editableResults.find((cell)=>{return cell.id==result.id})

        return (
            <>
                {editableCells[result.id]?.[field] ?
                    (<><form onSubmit={async (e)=>{
                        e.preventDefault();
                        await handleFieldConfirm();
                        handleCellClick(result.id, field)
                        }}>
                        <input style={{ color: "black", width: "75%" }}
                            value={currentResult?currentResult[field]:''}
                            onChange={(e: ChangeEvent<HTMLInputElement>) => {
                                handleFieldChange(result.id, field, e.target.value)
                            }
                            }
                        />
                        <button style={{ display: "inline", margin: "5px" }} type="button"
                            onClick={() => {
                                handleCellClick(result.id, field)
                            }
                            }
                        >
                            ×
                        </button>
                        <button style={{ display: "inline", margin: "5px" }} type="submit"
                            
                        >
                            ✔
                        </button>
                        </form>
                    </>)
                    :
                    (<>
                        {result[field]}
                        <button style={{ display: "inline" }} onClick={() => { handleCellClick(result.id, field) }}>
                            ✎
                        </button>
                    </>
                    )
                }
            </>)
    };

export default DynamicUserField;
