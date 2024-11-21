import React, { useEffect, useState } from 'react';
import Button from './../Button';
import SearchTitleField from './SearchTitleField';
import DOMPurify from 'dompurify';
import ShareModal from './modal/ShareModal';

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

    const [shareModalActive, setShareModalActive]= useState(false);
    return (
        <div>
            {shareModalActive?<ShareModal setShareModalActive={setShareModalActive} search_id={currentSearchId}></ShareModal>:<></>}
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
                <div className="shareButton text-right">
                    <Button className="bg-purple-700" onClick={()=>{ setShareModalActive(true)}}>
                        Share
                    </Button>
                </div>
            </div>
        </div>
    )
};

export default SearchHeader;
