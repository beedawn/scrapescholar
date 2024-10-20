import React, { Dispatch, SetStateAction, useState } from 'react';
import Button from './../Button';
import SearchBox from './SearchBox';
import DropdownSearchBox from './DropdownSearchBox';
import Dropdown from '../../types/DropdownType';
import SourcesAccordian from './SourcesAccordian';

import apiCalls from '@/app/api/apiCalls';
interface NavBarProps {
    handleResults: (event: React.FormEvent<HTMLFormElement>) => void;
    addInput: () => void;
    inputs: string[];
    handleSearchChange: (index: number,
        event: React.ChangeEvent<HTMLInputElement>) => void;
    handleDropdownChange: (index: number, option: Dropdown) => void;
    removeInput: (index: number) => void;
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
    dropdown: Dropdown[];
    addToUserDatabaseList: (item: string) => void;
    removeFromUserDatabaseList: (item: string) => void;
    searches: any[];
    handlePastSearchSelection:
    (event: React.ChangeEvent<HTMLSelectElement>) => void;
}

const NavBar: React.FC<NavBarProps> = ({ handleResults,
    addInput, inputs, handleSearchChange, removeInput,
    setLoggedIn, dropdown, handleDropdownChange,
    addToUserDatabaseList, removeFromUserDatabaseList,
    searches, handlePastSearchSelection }) => {

        const {deleteCookie}=apiCalls();
    const handleLogout = async () => {
        await deleteCookie();
        setLoggedIn(false);
    };
    const dropdown_values = Object.values(Dropdown);
    return (
        <>
            <div className="p-5 max-w-sm mr-auto float-left">
                <div className="float-right pb-6" data-testid="logout-button">
                    <Button onClick={handleLogout} className="" >
                        Logout
                    </Button>
                </div>
                <h1 className="text-4xl font-bold">ScrapeScholar</h1>
                <SourcesAccordian addToUserDatabaseList={addToUserDatabaseList}
                    removeFromUserDatabaseList={removeFromUserDatabaseList} />
                <DropdownSearchBox value="past search dropdown"
                    onDropdownChange={(selectedTitle) => 
                        handlePastSearchSelection(selectedTitle)} valueArray={searches}
                    className="w-full" />
                <form onSubmit={handleResults}>
                    <Button onClick={addInput} className="m-5">
                        +
                    </Button>
                    <Button type="submit">
                        Search
                    </Button>
                    {inputs.map((input: string, index: number) => {
                        return (<div key={index}>
                            <SearchBox value={input} onChange={(e) => 
                                { handleSearchChange(index, e) }} className="m-2" />
                            {index != 0
                                &&
                                <Button onClick={() => {
                                    removeInput(index)
                                }} className="m-1 text-sm bg-red-600">
                                    -
                                </Button>}<br />
                            {inputs.length > 1 && index != inputs.length - 1 && inputs[index].length > 0 &&
                                <DropdownSearchBox value={dropdown[index]} className="ml-2" onDropdownChange={(e) => {
                                    handleDropdownChange(index, e.target.value as Dropdown)
                                }} valueArray={dropdown_values}
                                />
                            }
                        </div>)
                    })}
                </form>
            </div>
        </>
    );
};

export default NavBar;
