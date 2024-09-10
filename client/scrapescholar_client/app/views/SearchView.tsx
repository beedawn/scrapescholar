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
    id:number;
    title:string;
    link:string;
    date:string;
    source:string;
}
const SearchView: React.FC<SearchViewProps> = ({ setLoggedIn, disableD3 = false }) => {
    const [results, setResults] = useState<ResultItem[]>([]);
    const [inputs, setInputs] = useState<string[]>(['']);
    const [bubbleInputs, setBubbleInputs] = useState<{ x: number, y: number, radius: number, color: string, label: string }[]>([]);
    const [joinedInputsString, setJoinedInputsString] = useState<string[]>([]);
    const [dropdown, setDropdown] = useState<Dropdown[]>([Dropdown.AND]);
    const [loading, setLoading]=useState<boolean>(false);
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
   const handleSubmit = async (event: { preventDefault: () => void; }) => {
        event.preventDefault();
        setLoading(true);
        const filterBlankInputs = inputs.filter((input)=>(input!==''))
        console.log(filterBlankInputs)
        let inputsAndLogicalOperators: string[] = [];
        for (let i = 0; i < filterBlankInputs.length; i++) {
            inputsAndLogicalOperators.push(filterBlankInputs[i]);
            if (i < filterBlankInputs.length - 1 && filterBlankInputs[i] != emptyString && filterBlankInputs.length > 1) {
                inputsAndLogicalOperators.push(dropdown[i])
            }
        }
        const inputsAndLogicalOperatorsString = inputsAndLogicalOperators.join(' ')
        setJoinedInputsString([inputsAndLogicalOperatorsString]);


      
            const newBubbleInputs = filterBlankInputs.map((input, i) => ({
              x: i,
              y: 50,
              radius: 50,
              color: "green",
              label: input
            }));
            setBubbleInputs(newBubbleInputs);
       

        let data:Response;
        let jsonData;
        if (inputsAndLogicalOperators.length === 0)
            setInputs([emptyString])
        else{
            setInputs([...filterBlankInputs])
            
            const apiQuery = inputsAndLogicalOperators.join('+')
  
            try{
            data = await fetch(`http://localhost:8000/sciencedirect?query=${apiQuery}`)
            jsonData = await data.json()
            }
            catch(error:any){
                jsonData = [{"title":error.message,link:''}]
            }
        }
        //run off and get results somewhere


        
       
        if(jsonData !== undefined && jsonData.length>0)
            setResults(jsonData)
        else
        //set better error message
            setResults([]);
            setLoading(false);
    }
    return (
        <div>
                <NavBar handleResults={handleSubmit} addInput={addInput} inputs={inputs} 
                handleSearchChange={handleSearchChange} removeInput={removeInput} setLoggedIn={setLoggedIn} dropdown={dropdown} handleDropdownChange={handleDropdownChange}/>
                {loading?<p>Loading</p>:<SearchResults displayInputs={joinedInputsString} results={results} emptyString={emptyString} disableD3={disableD3} inputs={inputs} bubbleInputs={bubbleInputs}/>}

        </div>
    );
}
export default SearchView;