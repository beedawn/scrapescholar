import React from 'react';
import LinePlot from './d3/LinePlot';

interface SearchResultsProps {
    children?: React.ReactNode;
    displayInputs: string[];
    results: string;
    onClick?: () => void;
    className?: string;
    emptyString?: string;
}

const SearchResults: React.FC<SearchResultsProps> = ({ children, results, displayInputs, onClick, className, emptyString }) => {
    return (
        <>
        <div style={{ maxWidth: "fit-content", padding: "50px", float: "left" }}>
            {results !== emptyString && displayInputs[0] !== emptyString ? (
                <>
                    <p>You searched {
                        displayInputs
                    }
                    </p>
                    <div> {results}</div>
                    <div>
                        <LinePlot data={[20, 40, 50, 60]} width={200} height={200} />
                    </div>
                </>
            ) : (
                results !== emptyString
                &&
                <p className="bg-red-800 p-2 rounded">
                    Please enter a keyword
                </p>
            )}
            </div>
        </>
    );
};

export default SearchResults;
