"use client";
import Image from "next/image";
import React, { useState, Dispatch,SetStateAction } from 'react';
import SearchResults from "../components/SearchResults";
import NavBar from "../components/NavBar";

interface SearchViewProps {
    setLoggedIn:Dispatch<SetStateAction<boolean>>;
    disableD3?:boolean;
  }

const SearchView : React.FC<SearchViewProps>=({setLoggedIn, disableD3=false}) => {
    const [results, setResults] = useState<string>('');
    const [inputs, setInputs] = useState<string[]>(['']);
    const [displayInputs, setDisplayInputs] = useState<string[]>([]);
    const emptyString = '';

    const addInput = () => {
        setInputs([...inputs, emptyString]);
    }

    const removeInput = (index: number) => {
        const newInput = inputs.filter((_, input_index) => input_index !== index)
        setInputs([...newInput]);
    }

    const handleSearchChange = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
        const newInputs = [...inputs];
        newInputs[index] = e.target.value;
        setInputs(newInputs);
    }

    const handleResults = (event: { preventDefault: () => void; }) => {
        event.preventDefault();
        //run off and get results somewhere
        setResults('No results found.');
        const filteredInputs = [...inputs].filter((input) => { return (input) })
        const stringFilteredInputs = filteredInputs.join(', ')
        setDisplayInputs([stringFilteredInputs]);
        if (filteredInputs.length === 0)
            setInputs([emptyString])
        else
            setInputs([...filteredInputs])
    }

    return (
        <div>
                <NavBar handleResults={handleResults} addInput={addInput} inputs={inputs} 
                handleSearchChange={handleSearchChange} removeInput={removeInput} setLoggedIn={setLoggedIn}/>
                <SearchResults displayInputs={displayInputs} results={results} emptyString={emptyString} disableD3={disableD3} />
        </div>
    );
}
export default SearchView;