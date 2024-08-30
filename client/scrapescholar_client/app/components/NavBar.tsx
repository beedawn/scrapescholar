import React from 'react';
import Button from './Button';
import SearchBox from './SearchBox';

interface NavBarProps {
    children?: React.ReactNode;
    onClick?: () => void;
    className?: string;
    type?: any;
    handleResults: (event: React.FormEvent<HTMLFormElement>) => void;
    addInput: () => void;
    inputs: string[];
    handleSearchChange: (index: number, event: React<HTMLInputElement>) => void;
    removeInput: (index: number) => void;
}

const NavBar: React.FC<NavBarProps> = ({ children, onClick, className, handleResults,
    addInput, inputs, handleSearchChange, removeInput }) => {
    return (
        <>
            <div style={{ maxWidth: "400px", padding: "50px", marginRight: "auto", float: "left" }}>
                <h1 className="text-4xl font-bold">ScrapeScholar</h1>
                <form onSubmit={handleResults}>
                    <Button onClick={addInput} className="m-5">+</Button>
                    <Button type="submit" >Search</Button>
                    {inputs.map((input: string, index: number) => {
                        return (<div key={index}>
                            <SearchBox value={input} onChange={(e) => { handleSearchChange(index, e) }} className="m-2 px-2 py-2 " />
                            {index != 0
                                &&
                                <Button onClick={() => {
                                    removeInput(index)
                                }} className="m-1 text-sm bg-red-600">
                                    -
                                </Button>}
                        </div>)
                    })}
                </form>
            </div>
        </>
    );
};

export default NavBar;
