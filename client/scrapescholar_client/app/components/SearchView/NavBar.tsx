import React, { Dispatch, SetStateAction, useState, useEffect } from 'react';
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

    useEffect(()=>{

        setOpenMenu(false)
    },[isMobile])


    return (
        <>
        {isMobile && !openMenu?<>
        <div className="flex"  data-testid="menu_bar"><div className="p-3" onClick={()=>{setOpenMenu(true)}}>
            <a href="#">
            <HamburgerIcon />
            </a>
            </div>
            <ScrapeScholarHeader />
            </div>
            </>
            :
            <>
            {isMobile?<div className="justify-items-end w-full pb-7" data-testid="nav_close_button" onClick={()=>{setOpenMenu(false)}}><Button className="bg-slate-600" > Close </Button></div>:<></>}
            <div className=" h-screen" data-testid="navbar">
                <div className="flex">
                <ScrapeScholarHeader />
                <div className="float-right pb-6 p-2" data-testid="logout-button">
                    <Button onClick={handleLogout} className="" >
                        Logout
                    </Button>
                </div>
                
                </div>
                <SourcesAccordian addToUserDatabaseList={addToUserDatabaseList}
                    removeFromUserDatabaseList={removeFromUserDatabaseList} />
                    <SettingsAccordian setOpenUserManagement={setOpenUserManagement} setDataFull={setDataFull} clearPages={clearPages} setOpenMenu={setOpenMenu}/>
                <DropdownSearchBox value="past search dropdown"
                    onDropdownChange={(selectedTitle) => {
                        handlePastSearchSelection(selectedTitle);setOpenMenu(false)}} valueArray={searches}
                    className="w-52"  defaultValue='Past Searches'/>
                <form onSubmit={(e)=>{handleResults(e);setOpenMenu(false)}}>
               <div className="flex">
                    <Button onClick={()=>{if(inputs.length<max_inputs){addInput()}}} className="m-5">
                        +
                    </Button>
                    <span data-testid="search_button">
                    <Button type="submit"className="mt-5">
                        Search
                    </Button>
                    
                    </span>
                    </div><div>
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
