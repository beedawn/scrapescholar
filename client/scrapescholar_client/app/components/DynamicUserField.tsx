import React, { ChangeEvent, useState } from 'react';
import Button from './Button';
import { ResultItem } from '../views/SearchView';
import {EditableCell} from './ResultsTable';
type EditableField = 'relevance' | 'methodology' | 'clarity' | 'completeness' | 'transparency';

interface DynamicUserFieldProps {
    field: EditableField;
    handleCellClick: (index:number, field: EditableField) => void;
    editableCells: EditableCell[];
    result:ResultItem;
    handleFieldChange:(index:number, field:keyof EditableCell, value:string) => void;
    handleFieldConfirm:()=>void;
    editableResults:ResultItem[];
}

const DynamicUserField: React.FC<DynamicUserFieldProps> = ({  field, handleCellClick, result, editableCells, handleFieldChange, handleFieldConfirm, editableResults }) => {
 

    
    return (
    <>
    {editableCells[result.id]?.[field]?
                            (<><input style={{color:"black"}} value={editableResults[result.id][field]} onChange={(e:ChangeEvent<HTMLInputElement>)=>{handleFieldChange(result.id,field,e.target.value)}} />
                            <button style={{display:"inline"}} onClick={()=>{
                                handleCellClick(result.id,field) 
                                }} >
                                    ×
                                    </button>
                                    <button style={{display:"inline"}} onClick={()=>{
                                handleFieldConfirm() 
                                handleCellClick(result.id,field)
                                }}>✔</button>
                                    </>)
                                    :
                                    (<>
                                    {result[field]}
                                    <div style={{display:"inline"}} onClick={()=>{handleCellClick(result.id,field)}}>
                                        ✎
                                        </div>
                                        </>)}
    </>)
};

export default DynamicUserField;
