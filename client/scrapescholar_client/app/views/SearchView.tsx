"use client";
import Image from "next/image";
import React, { useState, Dispatch,SetStateAction, } from 'react';
import SearchResults from "../components/SearchResults";
import NavBar from "../components/NavBar";
import Dropdown from "../types/DropdownType";
import { filter } from "d3";

interface SearchViewProps {
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
    disableD3?: boolean;
}

export interface ResultItem{
    title:string;
    link:string;
}
const SearchView: React.FC<SearchViewProps> = ({ setLoggedIn, disableD3 = false }) => {
    const [results, setResults] = useState<ResultItem[]>([]);
    const [inputs, setInputs] = useState<string[]>(['']);
    const [displayInputs, setDisplayInputs] = useState<string[]>([]);
    const [dropdown, setDropdown] = useState<Dropdown[]>([Dropdown.AND]);
    const emptyString = '';
    const addInput = () => {
        setInputs([...inputs, emptyString]);
        setDropdown([...dropdown, Dropdown.AND]);
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
    const handleDropdownChange = (index: number, option: Dropdown) => {
        const newDropdown = [...dropdown];
        newDropdown[index] = option;
        setDropdown(newDropdown);
    }
   const handleResults = async (event: { preventDefault: () => void; }) => {
        event.preventDefault();
        const filteredInputs = [...inputs].filter((input) => { return (input) })
        let combinedQuery: string[] = [];
        for (let i = 0; i < filteredInputs.length; i++) {
            combinedQuery.push(filteredInputs[i]);
            if (i < filteredInputs.length - 1 && filteredInputs[i] != emptyString && filteredInputs.length > 1) {
                combinedQuery.push(dropdown[i])
            }
        }
        const stringFilteredInputs = combinedQuery.join(' ')
        setDisplayInputs([stringFilteredInputs]);

        let data:Response;
        let posts = [];
        if (combinedQuery.length === 0)
            setInputs([emptyString])
        else{
            setInputs([...filteredInputs])
            try{
            data = await fetch('http://localhost:8000/sciencedirect?query=test')
            posts = await data.json()
            }
            catch(error:any){
                posts = [{"title":error.message,link:''}]
            }
        }
        //run off and get results somewhere


        
       
        if(posts.length>0)
            setResults(posts)
        else
            setResults([{title:"No results found", link:""}]);
    }
    return (
        <div>
                <NavBar handleResults={handleResults} addInput={addInput} inputs={inputs} 
                handleSearchChange={handleSearchChange} removeInput={removeInput} setLoggedIn={setLoggedIn} dropdown={dropdown} handleDropdownChange={handleDropdownChange}/>
                <SearchResults displayInputs={displayInputs} results={results} emptyString={emptyString} disableD3={disableD3} inputs={inputs} />

        </div>
    );
}
export default SearchView;