"use client";
import Image from "next/image";
import React, { useState, Dispatch, SetStateAction, } from 'react';
import SearchResults from "../components/SearchResults";
import NavBar from "../components/NavBar";
import Dropdown from "../types/DropdownType";
import { filter } from "d3";

interface SearchViewProps {
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
    disableD3?: boolean;
}

export interface ResultItem {
    id: number;
    title: string;
    link: string;
    date: string;
    source: string;
}

const SearchView: React.FC<SearchViewProps> = ({ setLoggedIn, disableD3 = false }) => {
    //gets data from api and stores in results
    const [results, setResults] = useState<ResultItem[]>([]);
    //inputs gets user inputs, update everytime user enters character
    const [inputs, setInputs] = useState<string[]>(['']);
    //bubble inputs is passed to bubble plot, pure inputs that update when Search is pressed only
    const [bubbleInputs, setBubbleInputs] = useState<{
        x: number,
        y: number,
        radius: number,
        color: string,
        label: string
    }[]>([]);
    //string of inputs joined with ' '
    const [joinedInputsString, setJoinedInputsString] = useState<string[]>([]);
    //drop down array for dropdown values
    const [dropdown, setDropdown] = useState<Dropdown[]>([Dropdown.AND]);
    //triggers when search is pressed so that UI is updated to loading
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<any>();
    //empty string variable to make code easier to read
    const emptyString = '';
    //adds input and drop down when plus is pressed
    const addInput = () => {
        setInputs([...inputs, emptyString]);
        setDropdown([...dropdown, Dropdown.AND]);
    }
    //removes input when minus is pressed
    const removeInput = (index: number) => {
        const newInput = inputs.filter((_, input_index) => input_index !== index)
        setInputs([...newInput]);
    }
    //updates inputs when input field is edited
    const handleSearchChange = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
        const newInputs = [...inputs];
        newInputs[index] = e.target.value;
        setInputs(newInputs);
    }
    //updates data in dropdown array when and/or/not is selected
    const handleDropdownChange = (index: number, option: Dropdown) => {
        const newDropdown = [...dropdown];
        newDropdown[index] = option;
        setDropdown(newDropdown);
    }
    //runs when search is pressed
    const handleSubmit = async (event: { preventDefault: () => void; }) => {
        //prevents default form submit which causes page to reload
        event.preventDefault();
        //sets loading to true which triggers "Loading" to show in UI
        setLoading(true);
        setError(null);
        //filters out empty input fields
        const filterBlankInputs = inputs.filter((input) => (input !== ''))
        //declare empty array to combien user inputs and values from drop downs
        let inputsAndLogicalOperators: string[] = [];
        //iterate through valid non blank inputs and append them and associated logical operator
        for (let i = 0; i < filterBlankInputs.length; i++) {
            //add input value
            inputsAndLogicalOperators.push(filterBlankInputs[i]);
            //make sure we aren't at end of array
            if (i < filterBlankInputs.length - 1
                //make sure there is more than 1 item in the inputs, if there is only one item we don't need a logical operator 
                && filterBlankInputs.length > 1) {
                //add logical operator under input field to array
                inputsAndLogicalOperators.push(dropdown[i])
            }
        }
        const inputsAndLogicalOperatorsString = inputsAndLogicalOperators.join(' ')
        setJoinedInputsString([inputsAndLogicalOperatorsString]);
        //can probably move this to bubbleplot
        const newBubbleInputs = filterBlankInputs.map((keyword, i) => ({
            //set x value as the index, because i dont know a better way to lay these out yet
            x: i,
            //all circles are on same y axis
            y: 50,
            //same radius
            radius: 50,
            //same color
            color: "green",
            //label is set to keyword
            label: keyword
        }));
        //update state with our new array
        setBubbleInputs(newBubbleInputs);
        //initialize data variable to fill up with api response
        let data: Response;
        let jsonData;
        if (inputsAndLogicalOperators.length === 0)
            setInputs([emptyString])
        else {
            setInputs([...filterBlankInputs])
            const apiQuery = inputsAndLogicalOperators.join('+')
            try {
                data = await fetch(`http://0.0.0.0:8000/scopus?query=${apiQuery}`)
                jsonData = await data.json()
            }
            catch (error: any) {
                // jsonData = [{ "title": error.message, link: '' }]
                setError(error);
            }
        }
        if (jsonData !== undefined && jsonData.length > 0) {
            setResults(jsonData)
        }
        else {
            //set better error message
            setResults([]);
        }
        setLoading(false);
    }
    return (
        <div>
            <NavBar handleResults={handleSubmit} addInput={addInput} inputs={inputs}
                handleSearchChange={handleSearchChange} removeInput={removeInput}
                setLoggedIn={setLoggedIn} dropdown={dropdown} handleDropdownChange={handleDropdownChange} />
            {error ? <p>{error.message}</p> : loading ? <p>Loading</p> :
                <SearchResults displayInputs={joinedInputsString}
                    results={results} emptyString={emptyString} disableD3={disableD3}
                    inputs={inputs} bubbleInputs={bubbleInputs} />}
        </div>
    );
}
export default SearchView;