import React, { useEffect } from 'react';
import Button from './../Button';
import SearchTitleField from './SearchTitleField';


interface SearchHeaderProps {
    downloadURL: string;
    searchName: string;
    setSearchName: (item: string) => void;
    currentSearchId: number;
    setLoading: (item: boolean) => void;
}
const SearchHeader: React.FC<SearchHeaderProps> = ({
    downloadURL, searchName, setSearchName,
    currentSearchId, setLoading }) => {
    return (
        <div>
            <div className="topContainer">
                <div className="searchName">

                    <SearchTitleField searchName={searchName}
                        setSearchName={setSearchName}
                        currentSearchId={currentSearchId}
                        setLoading={setLoading} />
                </div>
                <div className="downloadButton text-right">
                    <Button>
                        <a href={downloadURL}>Download</a>
                    </Button>
                </div>
            </div>
        </div>
    )
};

export default SearchHeader;
