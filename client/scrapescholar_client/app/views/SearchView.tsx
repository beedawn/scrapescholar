"use client";
import React, { useState, Dispatch, SetStateAction, useEffect } from 'react';
import SearchResults from "../components/SearchView/SearchResults";
import NavBar from "../components/SearchView/NavBar";
import Dropdown from "../types/DropdownType";
import apiCalls from '../api/apiCalls';
import DataFull from '../components/SearchView/DataFull';
import CommentsSidebar from '../components/SearchView/CommentsSidebar';
import Loading from '../components/Loading';
import UserManagement from '../components/UserManagement/UserManagement';
import Relevance from '../types/Relevance';
import DOMPurify from 'dompurify';
import windowWidth from '../components/responsive/windowWidth';

import { APIKeyInterface } from '../components/SearchView/modal/APIKeyModal';

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
    onArticleClick: (articleId: number) => Promise<void>;
}

const SearchView: React.FC<SearchViewProps> = ({ setLoggedIn, disableD3 = false }) => {
    const[APIKey, setAPIKey]=useState<APIKeyInterface>({scopus:"",sciencedirect:""});
    const [inputs, setInputs] = useState<string[]>(['']);
    const [currentSearchId, setCurrentSearchId] = useState<number>(-1);
    const [searchName, setSearchName] = useState("search name");
    const [loading, setLoading] = useState<boolean>(false);
    const { getAPIDatabases, getAPIResults, getAPISearches, getAPIPastSearchResults, getAPIPastSearchTitle } = apiCalls();
    const [selectedArticleId, setSelectedArticleId] = useState<number | null>(null);
    const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);
    const [openUserManagement, setOpenUserManagement] = useState<boolean>(false);
    const [relevanceChanged, setRelevanceChanged] = useState<boolean>(false);
    const [selectedSearchIdState, setSelectedSearchIdState] = useState<number>();
    const [width, setWidth] = useState<number>(window.innerWidth);
    const [isMobile, setIsMobile] = useState<boolean>(false)
    const sumResults = (results: ResultItem[], comparison: string) => {
        let sum = 0
        if (results !== undefined) {
            for (let result of results) {
                if (result.color == comparison) {
                    sum++;
                }
            }
        }
        return sum
    }
    useEffect(() => {
        windowWidth(setWidth)

        if (width < 768) {
            setIsMobile(true)
        } else {
            setIsMobile(false)
        }

    }, [width]);
    useEffect(() => {
        const fetchDatabases = async () => {
            const db_list = await getAPIDatabases();
            setUserDatabaseList(db_list);
        };
        const fetchSearches = async () => {
            const search_list = await getAPISearches(setError);
            setSearches(search_list);
        };
        fetchSearches();
        if (searches.length >= 300) {
            setDataFull(true)
        } else {
            setDataFull(false)
        }
        fetchDatabases();
    }, [loading]);
    const [results, setResults] = useState<ResultItem[]>([]);
    const [dataFull, setDataFull] = useState<boolean>(false);
    const [isCommentButtonPressed, setIsCommentButtonPressed] = useState(false);
    const initBubblePlotData = (fetchResults: ResultItem[]) => {
        const possible_types = Object.keys(Relevance).filter((key) => isNaN(Number(key)));
        let data_array = []
        let color = {
            "Relevant": "green",
            "SemiRelevant": "#FF8C00",
            "Not Relevant": "red"
        }
        for (let type of possible_types) {
            if (type == "NotRelevant") {
                type = "Not Relevant"
            }
            data_array.push({
                "name": type,
                "sum": sumResults(fetchResults, type),
                "color": color[type as keyof typeof color]
            })
        }
        let divider;
        if (fetchResults !== undefined) {
            divider = fetchResults.length
        }
        else {
            divider = 25
        }
        const newBubbleInputs = data_array.map((keyword, i) => ({
            x: i < 2 ? i * .5 : 0,
            //all circles are on same y axis
            y: i + i * 50,
            radius: (keyword.sum / divider) * 50,
            color: keyword.color,
            label: `${keyword.name} ${keyword.sum}`
        }));
        return newBubbleInputs;
    }

    useEffect(() => {
        const getResults = async () => {
            if (selectedSearchIdState) {
                const fetchResults = await getAPIPastSearchResults(setResults, setError, selectedSearchIdState);
                const newBubbleInputs = initBubblePlotData(fetchResults);
                setBubbleInputs(newBubbleInputs);
            }
        }
        getResults()
    }, [relevanceChanged])
    const [bubbleInputs, setBubbleInputs] = useState<{
        x: number,
        y: number,
        radius: number,
        color: string,
        label: string
    }[]>([]);
    const [userDatabaseList, setUserDatabaseList] = useState<string[]>([]);
    const addToUserDatabaseList = (item: string) => {
        setUserDatabaseList([...userDatabaseList, item])
    }
    const removeFromUserDatabaseList = (item: string) => {
        setUserDatabaseList(userDatabaseList.filter((array_item: any) => { return array_item != item }))
    }

    //string of inputs joined with ' '
    const [joinedInputsString, setJoinedInputsString] = useState<string[]>([]);
    //drop down array for dropdown values
    const [dropdown, setDropdown] = useState<Dropdown[]>([Dropdown.AND]);

    const [error, setError] = useState<any>();
    const [searches, setSearches] = useState<any[]>([]);
    const emptyString = '';
    //adds input and drop down when plus is pressed
    const addInput = () => {
        setInputs([...inputs, emptyString]);
        setDropdown([...dropdown, Dropdown.AND]);
    }
    const removeInput = (index: number) => {
        const newInput = inputs.filter((_, input_index) => input_index !== index)
        setInputs([...newInput]);
    }
    const handleSearchChange = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
        const sanitizedValue = DOMPurify.sanitize(e.target.value);
        const newInputs = [...inputs];
        newInputs[index] = sanitizedValue;
        setInputs(newInputs);
    }
    const clearPages = () => {
        setOpenUserManagement(false)
        setDataFull(false)
        setLoading(false);
    }
    const handlePastSearchSelection = async (event: any) => {
        const selectedSearchId = event.target.value;
        await handlePastSearchSelectionSearchID(selectedSearchId)
    }
    const handlePastSearchSelectionSearchID = async (search_id: number) => {
        setCurrentSearchId(search_id)
        setSelectedSearchIdState(search_id)
        setDataFull(false)
        if (search_id) {
            clearPages();
            setError(null);
            const search_results = await getAPIPastSearchResults(setResults, setError, search_id);
            await getAPIPastSearchTitle(search_id, setSearchName, setJoinedInputsString)
            clearPages();
            const bubble_data = initBubblePlotData(search_results)
            setBubbleInputs(bubble_data);
        }
        else {
            setError({ "message": "No search found" });
        }

    }
    const handleDropdownChange = (index: number, option: Dropdown) => {
        const newDropdown = [...dropdown];
        newDropdown[index] = option;
        setDropdown(newDropdown);
    }
    const handleArticleClick = async (articleId: number) => {
        setSelectedArticleId(articleId);
        setIsSidebarOpen(true);
    };

    const handleSubmit = async (event: { preventDefault: () => void; }) => {
        event.preventDefault();
        setLoading(true);
        setError(null);
        setDataFull(false);
        setOpenUserManagement(false);
        setIsSidebarOpen(false);
        const filterBlankInputs = inputs.filter((input) => (input !== ''))
        let inputsAndLogicalOperators: string[] = [];
        for (let i = 0; i < filterBlankInputs.length; i++) {
            inputsAndLogicalOperators.push(filterBlankInputs[i]);
            if (i < filterBlankInputs.length - 1 && filterBlankInputs.length > 1) {
                if (dropdown[i] == "NOT") {
                    inputsAndLogicalOperators.push("AND")
                }
                inputsAndLogicalOperators.push(dropdown[i])
            }
        }
        const inputsAndLogicalOperatorsString = inputsAndLogicalOperators.join(' ')
        setJoinedInputsString([inputsAndLogicalOperatorsString]);
        const responseResult = await getAPIResults(userDatabaseList,
            inputsAndLogicalOperators, emptyString,
            setInputs, setResults, setError,
            filterBlankInputs, inputs,
            setDataFull, setCurrentSearchId, APIKey);
        const bubblePlot = initBubblePlotData(responseResult.articles)
        setBubbleInputs(bubblePlot)
        setSelectedSearchIdState(responseResult.search_id)
        setLoading(false);
    }
    return (
        <div className="flex md:flex-row flex-col pb-10 h-screen ">
            <div className=" xs:w-full  md: w-1/4 lg:w-1/4 xl:w-1/5 p-5">
                <NavBar handleResults={handleSubmit} addInput={addInput} inputs={inputs}
                    handleSearchChange={handleSearchChange} removeInput={removeInput}
                    setLoggedIn={setLoggedIn} dropdown={dropdown} handleDropdownChange={handleDropdownChange}
                    addToUserDatabaseList={addToUserDatabaseList} removeFromUserDatabaseList={removeFromUserDatabaseList}
                    searches={searches} handlePastSearchSelection={handlePastSearchSelection}
                    setOpenUserManagement={setOpenUserManagement}
                    setDataFull={setDataFull} clearPages={clearPages} isMobile={isMobile}
                    setAPIKey={setAPIKey} APIKey={APIKey}
                />
            </div>
            <div className={`flex-1 ${!isMobile ? 'm-10, ml-12' : 'm-2 p-2'} overflow-auto ${isMobile && isSidebarOpen && selectedArticleId !== null && isCommentButtonPressed ? 'hidden' : ''}`}>
                {error ? (<p>{error.message}</p>)
                    : loading ? <Loading /> : openUserManagement ? <><UserManagement /></> :
                        dataFull ? <> <DataFull searches={searches} setLoading={setLoading} /></> :
                            <SearchResults
                                setResults={setResults}
                                displayInputs={joinedInputsString}
                                setLoading={setLoading}
                                results={results}
                                emptyString={emptyString}
                                disableD3={disableD3}
                                bubbleInputs={bubbleInputs}
                                searchName={searchName}
                                setSearchName={setSearchName}
                                currentSearchId={currentSearchId}
                                setDisplayInputs={setJoinedInputsString}
                                onArticleClick={handleArticleClick}
                                setRelevanceChanged={setRelevanceChanged}
                                relevanceChanged={relevanceChanged}
                                handlePastSearchSelectionSearchID={handlePastSearchSelectionSearchID}
                                isMobile={isMobile}
                            />}
            </div>
            {isSidebarOpen && selectedArticleId !== null && (
                <CommentsSidebar articleId={selectedArticleId} onClose={() => {
                    if (isMobile) {
                        setIsCommentButtonPressed(false)
                    } else {
                        setIsSidebarOpen(false);
                    }
                }} isMobile={isMobile}
                    setIsCommentButtonPressed={setIsCommentButtonPressed}
                    isCommentButtonPressed={isCommentButtonPressed} />
            )}
        </div>
    );
}
export default SearchView;