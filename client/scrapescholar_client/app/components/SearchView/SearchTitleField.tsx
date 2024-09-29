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
                setEditable(!editable)

            }
        return (
            <><div data-testid="search-title">
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
                        <span>{searchName}</span>
                        <button style={{ display: "inline" }} onClick={handleClick }>
                            ✎
                        </button>
                    </>
                    )
                }
              </div>  
            </>)
    };

export default SearchTitleField;
