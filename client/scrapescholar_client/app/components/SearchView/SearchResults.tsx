import React, { useState, useEffect } from 'react';
import BubblePlot from './../d3/BubblePlot';
import { ResultItem } from '../../views/SearchView';
import SearchHeader from './SearchHeader';
import ResultsTable from './ResultsTable';
import apiCalls from '@/app/api/apiCalls';
import CommentsSidebar from './CommentsSidebar'; // Import the CommentsSidebar component

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
}

const SearchResults: React.FC<SearchResultsProps> = ({
    results, displayInputs, className, emptyString,
    disableD3 = false, bubbleInputs, setResults,
    setSearchName, searchName, currentSearchId, setDisplayInputs,
    setLoading }) => {
    const [selectedArticle, setSelectedArticle] = useState<number | null>(null);
    const { getAPIPastSearchTitle, getCommentsByArticle } = apiCalls();

    const [comments, setComments] = useState<any[]>([]); // Comments state
    const [commentsLoading, setCommentsLoading] = useState<boolean>(false);     

    useEffect(() => {
        const fetchSearchName = async () => {
            await getAPIPastSearchTitle(
                currentSearchId, setSearchName, setDisplayInputs
            )
        }
        fetchSearchName();
    }, [])

    const onArticleClick = (articleId: number) => {
        console.log('Article clicked:', articleId);
        setSelectedArticle(articleId); // Set the selected article
    };    

    // const onArticleClick = async (articleId: number) => {
    //     // Log the articleId and trace the method call stack
    //     console.trace('onArticleClick called for articleId:', articleId);
    
    //     try {
    //         console.log('Fetching comments for article:', articleId);
            
    //         // Set loading state for comments
    //         setCommentsLoading(true);
    //         console.log('Comments loading set to true');
    
    //         // Fetch comments for the clicked article (assuming you have this API function defined)
    //         const fetchedComments = await getCommentsByArticle(articleId);
    
    //         console.log('Comments fetched:', fetchedComments);
    
    //         // Update the state with fetched comments
    //         setComments(fetchedComments);
    //         console.log('Comments state updated with fetched data');
    
    //         // Set the selected article ID to show comments in the sidebar
    //         setSelectedArticle(articleId);
    //         console.log('Selected articleId set:', articleId);
    
    //         // Stop the loading state after fetching comments
    //         setCommentsLoading(false);
    //         console.log('Comments loading set to false');
    
    //     } catch (err) {
    //         console.error('Error fetching comments for articleId:', articleId);
    //         console.trace(err); // Log the error and trace where it occurred
    
    //         // Stop loading state even if there's an error
    //         setCommentsLoading(false);
    //         console.log('Comments loading set to false after error');
    //     }
    // };
    

    return (
        <div className={className}>
            <div className="float-left p-12 max-w-md 
            sm:max-w-screen-xs md:max-w-screen-xs 
            lg:max-w-screen-md xl:max-w-screen-lg">
                {results.length !== 0 ? (
                    <div>
                        <SearchHeader downloadURL="/csv"
                            searchName={searchName} setSearchName={setSearchName}
                            currentSearchId={currentSearchId} setLoading={setLoading} />
                        <p>
                            You searched {displayInputs}
                        </p>
                        <div>
                            {disableD3 ? (<></>) : (<>
                                <BubblePlot data={bubbleInputs} /></>)}
                        </div>
                        <ResultsTable setResults={setResults}
                            results={results}
                            selectedArticle={selectedArticle}
                            setSelectedArticle={setSelectedArticle} 
                            setLoading={setLoading} 
                            onArticleClick={onArticleClick} />
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
            {/* Comments Sidebar */}
            <div className="w-1/4 bg-gray-100">
                {selectedArticle && (
                    <CommentsSidebar articleId={selectedArticle} />
                )}
            </div>            
        </div>
    );
};

export default SearchResults;