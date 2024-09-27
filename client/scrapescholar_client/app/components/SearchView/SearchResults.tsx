import React, { useState } from 'react';
import BubblePlot from './../d3/BubblePlot';
import { ResultItem } from '../../views/SearchView';
import SearchHeader from './SearchHeader';
import ResultsTable from './ResultsTable';
interface SearchResultsProps {
    displayInputs: string[];
    results: ResultItem[];
    className?: string;
    emptyString?: string;
    disableD3?: boolean;
    inputs: string[];
    bubbleInputs: { x: number, y: number, radius: number, color: string, label: string }[];
    setResults: (item: ResultItem[]) => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, displayInputs, className, emptyString,
    disableD3 = false, inputs, bubbleInputs, setResults }) => {
    const [selectedArticle, setSelectedArticle] = useState(-1);
    const [searchName, setSearchName]=useState("search name");
    return (
        <div className={className}>
            <div className="float-left p-12 max-w-md sm:max-w-screen-xs md:max-w-screen-xs lg:max-w-screen-md xl:max-w-screen-lg">
                {results.length !== 0 && displayInputs[0] !== emptyString ? (
                    <div>
                        <SearchHeader downloadURL="/csv" searchName={searchName} setSearchName={setSearchName} />
                        <p>
                            You searched {displayInputs}
                        </p>
                        <div>
                            {disableD3 ? (<></>) : (<>
                                <BubblePlot data={bubbleInputs}></BubblePlot></>)}
                        </div>
                        <ResultsTable setResults={setResults} results={results} selectedArticle={selectedArticle} setSelectedArticle={setSelectedArticle} />
                    </div>
                ) :
                    results.length === 0 && displayInputs[0] === ''
                        ?
                        (<p className="bg-red-800 p-2 rounded">
                            Please enter a keyword
                        </p>)
                        : (results.length === 0 && displayInputs[0] !== '' ? (<p>No Results Found</p>) : (<p>Loading...</p>))}
            </div>
        </div>
    );
};

export default SearchResults;
