import React, { Dispatch, SetStateAction, useState } from 'react';
import Button from './../Button';
import SearchBox from './SearchBox';
import DropdownSearchBox from './DropdownSearchBox';
import Dropdown from '../../types/DropdownType';
import SourcesAccordian from './SourcesAccordian';
import apiCalls from '@/app/api/apiCalls';
import SettingsAccordian from './SettingsAccordion';
import ScrapeScholarHeader from './ScrapeScholarHeader';
import HamburgerIcon from '../HamburgerIcon';
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
    setOpenUserManagement: (item:boolean)=>void;
    setDataFull: (item:boolean)=>void;
    clearPages:()=>void;
    isMobile:boolean;
}

const NavBar: React.FC<NavBarProps> = ({ handleResults,
    addInput, inputs, handleSearchChange, removeInput,
    setLoggedIn, dropdown, handleDropdownChange,
    addToUserDatabaseList, removeFromUserDatabaseList,
    searches, handlePastSearchSelection, setOpenUserManagement, setDataFull,clearPages,isMobile }) => {

        const {deleteCookie}=apiCalls();
    const handleLogout = async () => {
        await deleteCookie();
        setLoggedIn(false);
    };
    const [openMenu, setOpenMenu]= useState(false);
    const dropdown_values = Object.values(Dropdown);
    const max_inputs = 20



    return (
        <>
        {isMobile && !openMenu?<>
        <div className="flex"><div className="p-3" onClick={()=>{setOpenMenu(true)}}>
            <HamburgerIcon />
            </div>
            <ScrapeScholarHeader />
            </div>
            </>
            :
            <>
            {isMobile?<div onClick={()=>{setOpenMenu(false)}}>close</div>:<></>}
            <div className=" h-screen">
                <div className="flex">
                <div className="float-right pb-6 p-2" data-testid="logout-button">
                    <Button onClick={handleLogout} className="" >
                        Logout
                    </Button>
                </div>
                <ScrapeScholarHeader />
                </div>
                <SourcesAccordian addToUserDatabaseList={addToUserDatabaseList}
                    removeFromUserDatabaseList={removeFromUserDatabaseList} />
                    <SettingsAccordian setOpenUserManagement={setOpenUserManagement} setDataFull={setDataFull} clearPages={clearPages} setOpenMenu={setOpenMenu}/>
                <DropdownSearchBox value="past search dropdown"
                    onDropdownChange={(selectedTitle) => 
                        handlePastSearchSelection(selectedTitle)} valueArray={searches}
                    className="w-52"  defaultValue='Past Searches'/>
                <form onSubmit={(e)=>{handleResults(e);setOpenMenu(false)}}>
               
                    <Button onClick={()=>{if(inputs.length<max_inputs){addInput()}}} className="m-5">
                        +
                    </Button>
                    <span data-testid="search_button">
                    <Button type="submit">
                        Search
                    </Button>
                    </span><div>
                    {inputs.length>max_inputs-1?<>Maximum 20 keywords allowed.</>:<></>}
                    </div>
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
            </>}
        </>
    );
};

export default NavBar;
