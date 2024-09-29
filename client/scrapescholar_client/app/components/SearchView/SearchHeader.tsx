import React from 'react';
import Button from './../Button'; 
import SearchTitleField from './SearchTitleField';

interface SearchHeaderProps {
    downloadURL: string;
    searchName:string;
    setSearchName: (item: string) => void;
}
const SearchHeader: React.FC<SearchHeaderProps> = ({ downloadURL, searchName, setSearchName }) => {
    return (
        <div>
            <div className="topContainer">
                <div className="searchName">
                    
                    <SearchTitleField searchName={searchName} setSearchName={setSearchName}/></div>
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
