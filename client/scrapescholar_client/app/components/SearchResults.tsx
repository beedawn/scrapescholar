import React from 'react';
import LinePlot from './d3/LinePlot';

interface SearchResultsProps {
    displayInputs: string[];
    results: string;
    className?: string;
    emptyString?: string;
    disableD3?: boolean;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, displayInputs, className, emptyString, disableD3 = false }) => {
    return (
        <div className={className}>
            <div className="float-left p-12 max-w-fit">
                {results !== emptyString && displayInputs[0] !== emptyString ? (
                    <div>
                        <p>
                            You searched {displayInputs}
                        </p>
                        <div>
                            {results}
                        </div>
                        <div>
                            {disableD3 ? (<></>) : (<LinePlot data={[20, 40, 50, 60]} width={200} height={200} />)}
                        </div>
                    </div>
                ) : (
                    results !== emptyString
                    &&
                    <p className="bg-red-800 p-2 rounded">
                        Please enter a keyword
                    </p>
                )}
            </div>
        </div>
    );
};

export default SearchResults;
