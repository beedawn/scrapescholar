import React, { useState, useEffect } from 'react';
import BubblePlot from './../d3/BubblePlot';
import { ResultItem } from '../../views/SearchView';
import SearchHeader from './SearchHeader';
import ResultsTable from './ResultsTable';
import apiCalls from '@/app/api/apiCalls';
import ArticleModal from '../../components/SearchView/modal/ArticleModal';
import Button from '../Button';

interface SearchResultsProps {
    displayInputs: string[];
    results: ResultItem[];
    className?: string;
    emptyString?: string;
    disableD3?: boolean;
    bubbleInputs: { x: number, y: number, radius: number, color: string, label: string }[];
    setResults: (item: ResultItem[]) => void;
    setSearchName: (item: string) => void;
    searchName: string;
    currentSearchId: number;
    setDisplayInputs: (item: string[]) => void;
    setLoading: (item: boolean) => void;
    onArticleClick: (articleId: number) => Promise<void>;
    setRelevanceChanged: (item: boolean) => void;
    relevanceChanged: boolean;
}

const SearchResults: React.FC<SearchResultsProps> = ({
    results, displayInputs, className, emptyString,
    disableD3 = false, bubbleInputs, setResults,
    setSearchName, searchName, currentSearchId, setDisplayInputs,
    setLoading, onArticleClick, setRelevanceChanged, relevanceChanged }) => {
    const [selectedArticle, setSelectedArticle] = useState<number | null>(null);
    const { getAPIPastSearchTitle, getCommentsByArticle, downloadURL } = apiCalls();
    const [comments, setComments] = useState<any[]>([]); // Comments state
    const [commentsLoading, setCommentsLoading] = useState<boolean>(false);
    const [addArticleOpen, setAddArticleOpen] = useState<boolean>(false);

    useEffect(() => {
        const fetchSearchName = async () => {
            await getAPIPastSearchTitle(
                currentSearchId, setSearchName, setDisplayInputs
            )
        }
        fetchSearchName();
    }, [])

    const addArticleView = () => {
        setAddArticleOpen(!addArticleOpen)
    }

    return (
        <div className={className}>
            {addArticleOpen ? <ArticleModal addArticleView={addArticleView} search_id={currentSearchId}/> : <></>}
            <div className="float-left p-12 max-w-md 
            sm:max-w-screen-xs md:max-w-screen-sm 
            lg:max-w-screen-md xl:max-w-screen-lg">
                {results.length !== 0 ? (
                    <div>
                        <SearchHeader downloadURL={`${downloadURL}${currentSearchId}`}
                            searchName={searchName} setSearchName={setSearchName}
                            currentSearchId={currentSearchId} setLoading={setLoading} />
                        <p>
                            You searched {displayInputs}
                        </p>
                        <div>
                            {disableD3 ? (<></>) : (<>
                                <BubblePlot data={bubbleInputs} /></>)}
                        </div>
                        <div className="w-full text-right p-5">
                            <Button onClick={() => { addArticleView() }}>
                                Add Document
                            </Button>
                        </div>
                        <ResultsTable setResults={setResults}
                            results={results}
                            selectedArticle={selectedArticle}
                            setSelectedArticle={setSelectedArticle}
                            setLoading={setLoading}
                            onArticleClick={onArticleClick}
                            setRelevanceChanged={setRelevanceChanged}
                            relevanceChanged={relevanceChanged} />
                    </div>
                ) :
                    results.length === 0 && displayInputs[0] === ''
                        ?
                        (<p className="bg-red-800 p-2 rounded">
                            Please enter a keyword
                        </p>)
                        : (results.length === 0 && displayInputs[0] !== '' ?
                            (<p>No Results Found. Please try another search!</p>) :
                            (<p>Loading...</p>))}
            </div>
        </div>
    );
};

export default SearchResults;