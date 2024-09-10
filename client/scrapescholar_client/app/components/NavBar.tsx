import React, { Dispatch, SetStateAction } from 'react';
import Button from './Button';
import SearchBox from './SearchBox';
import DropdownSearchBox from './DropdownSearchBox';
import Dropdown from '../types/DropdownType';
interface NavBarProps {
    handleResults: (event: React.FormEvent<HTMLFormElement>) => void;
    addInput: () => void;
    inputs: string[];
    handleSearchChange: (index: number, event: React.ChangeEvent<HTMLInputElement>) => void;
    handleDropdownChange: (index: number, option: Dropdown) => void;
    removeInput: (index: number) => void;
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
    dropdown: Dropdown[];
}

const NavBar: React.FC<NavBarProps> = ({ handleResults,
    addInput, inputs, handleSearchChange, removeInput, setLoggedIn, dropdown, handleDropdownChange }) => {
    const handleLogout = () => {
        setLoggedIn(false);
    };
    return (
        <>
<<<<<<< HEAD
            <div className="p-5 max-w-md mr-auto float-left">
=======
            <div className="p-5 max-w-sm mr-auto float-left">
>>>>>>> 29-us-11--fr-11---the-system-shall-provide-a-field-in-the-results-that-shows-the-source-link-for-each-academic-article
                <div className="float-right pb-6" >
                    <Button onClick={handleLogout} className="">Logout</Button>
                </div>
                <h1 className="text-4xl font-bold">ScrapeScholar</h1>
                <form onSubmit={handleResults}>
                    <Button onClick={addInput} className="m-5">+</Button>
                    <Button type="submit" >Search</Button>
                    {inputs.map((input: string, index: number) => {
                        return (<div key={index}>
                            <SearchBox value={input} onChange={(e) => { handleSearchChange(index, e) }} className="m-2" />
                            {index != 0
                                &&
                                <Button onClick={() => {
                                    removeInput(index)
                                }} className="m-1 text-sm bg-red-600">
                                    -
                                </Button>}<br />
                            {inputs.length > 1 && index != inputs.length - 1 && inputs[index].length > 0 &&
                                <DropdownSearchBox value={dropdown[index]} className="ml-2" onDropdownChange={(e) => { handleDropdownChange(index, e.target.value as Dropdown) }}></DropdownSearchBox>}

                        </div>)
                    })}
                </form>
            </div>
        </>
    );
};

export default NavBar;
