import React, { ChangeEvent, useState } from 'react';
import { ResultItem } from '../../views/SearchView';
import { EditableCell } from './ResultsTable';
type EditableField = 'relevance' | 'methodology' | 'clarity' | 'completeness' | 'transparency';

interface SearchTitleFieldProps{

    searchName: string;
    setSearchName: (item: string) => void;
    
}


const SearchTitleField: React.FC<SearchTitleFieldProps> =
    ({  searchName, setSearchName
         }) => {
            const [editableSearchName,setEditableSearchName]=useState(searchName);

            const [editable, setEditable] = useState(false);
            const handleClick= ()  =>{
                console.log(editable)
                setEditable(!editable)

            }
        return (
            <>
                {editable ?
                    (<><form onSubmit={async (e)=>{
                        e.preventDefault();
                        handleClick()
                        }}>
                        <input style={{ color: "black", width: "50%" }}
                            value={editableSearchName}
                            onChange={(e)=>{setEditableSearchName(e.target.value)}}
                        />
                        <button style={{ display: "inline", margin: "5px" }} type="button"
                            onClick={()=>{
                                handleClick();
                                setEditableSearchName(searchName)
                            }
                            }
                        >
                            ×
                        </button>
                        <button style={{ display: "inline", margin: "5px" }} type="submit"
                            onClick={()=>{setSearchName(editableSearchName)}}
                        >
                            ✔
                        </button>
                        </form>
                    </>)
                    :
                    (<>
                        {searchName}
                        <button style={{ display: "inline" }} onClick={handleClick }>
                            ✎
                        </button>
                    </>
                    )
                }
            </>)
    };

export default SearchTitleField;
