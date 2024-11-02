import React, { useEffect } from 'react';
import Button from './../Button';
import SearchTitleField from './SearchTitleField';
import DOMPurify from 'dompurify';


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
    const sanitizedDownloadURL = DOMPurify.sanitize(downloadURL);
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
                        <a href={sanitizedDownloadURL}>Download</a>
                    </Button>
                </div>
            </div>
        </div>
    )
};

export default SearchHeader;
