import React, { useState } from 'react';
import apiCalls from '@/app/api/apiCalls';
interface SearchTitleFieldProps {
    searchName: string;
    setSearchName: (item: string) => void;
    currentSearchId: number;
    setLoading: (item: boolean) => void;
}

const SearchTitleField: React.FC<SearchTitleFieldProps> =
    ({ searchName, setSearchName, currentSearchId, setLoading
    }) => {
        const { putSearchTitle } = apiCalls();
        const putSearchName = async () => {
            await putSearchTitle(searchName,
                currentSearchId, setSearchName, setLoading)
        }
        const [editableSearchName, setEditableSearchName] = useState(searchName);
        const [editable, setEditable] = useState(false);
        const handleClick = () => {
            setEditable(!editable)
        }
        return (
            <><div data-testid="search-title">
                {editable ?
                    (<><form onSubmit={async (e) => {
                        e.preventDefault();
                        await putSearchName();
                        handleClick()
                    }}>
                        <input style={{ color: "black", width: "50%" }}
                            value={editableSearchName}
                            onChange={(e) => { setEditableSearchName(e.target.value) }}
                        />
                        <button style={{ display: "inline", margin: "5px" }} type="button"
                            onClick={() => {
                                handleClick();
                                setEditableSearchName(searchName)
                            }}
                        >
                            ×
                        </button>
                        <button style={{ display: "inline", margin: "5px" }} type="submit"
                            onClick={() => { setSearchName(editableSearchName); }}
                        >
                            ✔
                        </button>
                    </form>
                    </>)
                    :
                    (<>
                        <span data-testid="search-title-span">{searchName}</span>
                        <button style={{ display: "inline" }} onClick={handleClick}>
                            ✎
                        </button>
                    </>
                    )
                }
            </div>
            </>)
    };

export default SearchTitleField;
