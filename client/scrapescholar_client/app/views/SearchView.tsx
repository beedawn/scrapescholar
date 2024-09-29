"use client";
import React, { useState, Dispatch, SetStateAction, useEffect} from 'react';
import SearchResults from "../components/SearchView/SearchResults";
import NavBar from "../components/SearchView/NavBar";
import Dropdown from "../types/DropdownType";
import { queryAllByAltText } from '@testing-library/react';
import apiCalls from '../api/apiCalls'; 
import { filter } from 'd3';

interface SearchViewProps {
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
    disableD3?: boolean;
}

export interface ResultItem {
    [key: string]: any;
    id: number;
    title: string;
    link: string;
    date: string;
    source: string;
    citedby: number;
    color: string;
    relevance_score: number;
    abstract: string;
    document_type: string;
    evaluation_criteria: string;
    methodology: string;
    clarity: string;
    completeness: string;
    transparency: string;
}

const SearchView: React.FC<SearchViewProps> = ({ setLoggedIn, disableD3 = false }) => {

    const { getAPIDatabases, postAPILogin, getAPIResults } = apiCalls();

      useEffect(() => {
        const fetchDatabases = async () => {
            const db_list = await getAPIDatabases();
            setUserDatabaseList(db_list);  
 
    
        };
        fetchDatabases();  
    }, []); 

    const [searchName, setSearchName]=useState("search name");
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
    //list of user selected databases
    const [userDatabaseList, setUserDatabaseList] = useState<string[]>([]);

    const addToUserDatabaseList = (item:string) => {
       setUserDatabaseList ([...userDatabaseList, item])
    }
    const removeFromUserDatabaseList = (item:string) => {
       setUserDatabaseList(userDatabaseList.filter((array_item:any)=>{return array_item!=item}))
     }
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
       // console.log(userDatabaseList);
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
 
        await getAPIResults( userDatabaseList, inputsAndLogicalOperators, emptyString, setInputs, setResults, setError, filterBlankInputs);
        setLoading(false);
    }
    return (
        <div className="flex flex-col sm:flex-row sm:mx-12">
            <div className="w-full sm:w-1/3 lg:w-1/4 xl:w-1/5">
                <NavBar handleResults={handleSubmit} addInput={addInput} inputs={inputs}
                    handleSearchChange={handleSearchChange} removeInput={removeInput}
                    setLoggedIn={setLoggedIn} dropdown={dropdown} handleDropdownChange={handleDropdownChange} 
                    addToUserDatabaseList={addToUserDatabaseList} removeFromUserDatabaseList={removeFromUserDatabaseList}
                    />
            </div>
            <div className="flex-1 sm:mx-12 w-full">
                {error ? <p>{error.message}</p> : loading ? <p>Loading</p> :
                    <SearchResults setResults={setResults} displayInputs={joinedInputsString}
                        results={results} emptyString={emptyString} disableD3={disableD3}
                        inputs={inputs} bubbleInputs={bubbleInputs} searchName={searchName} setSearchName={setSearchName}/>}
            </div>
        </div>
    );
}
export default SearchView;