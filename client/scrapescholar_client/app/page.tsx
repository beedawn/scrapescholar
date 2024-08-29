"use client";
import Image from "next/image";
import React, { useState } from 'react';
import Button from './components/Button';
import SearchBox from "./components/SearchBox";
export default function Home() {
  const [results, setResults] = useState('');
  const [inputs, setInputs] = useState(['']);
  const [displayInputs, setDisplayInputs] = useState<string[]>([]);

  const addInput = () => {
    setInputs([...inputs, '']);
  }
  const removeInput = (index: number) => {
    const newInput = inputs.filter((_,input_index)=> input_index !== index)
    setInputs([...newInput]);
  }


  const handleSearchChange = (index: number, e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newInputs = [...inputs];
    newInputs[index] = e.target.value;
    setInputs(newInputs);

  }

  const handleResults = (event: { preventDefault: () => void; }) => {
    event.preventDefault();
    //run off and get results somewhere
    setResults('No results found.');
    const filteredInputs = [...inputs].filter((input)=>{return(input)})
    const stringFilteredInputs = filteredInputs.join(', ')
    setDisplayInputs([stringFilteredInputs]);
    if (filteredInputs.length ===0)
      setInputs([''])
    else
      setInputs([...filteredInputs])
  }
  return (
    <div>
      <div style={{ maxWidth: "25%", padding: "50px", marginRight: "auto", float: "left" }}>
        <h1 className="text-4xl font-bold">ScrapeScholar</h1>
        <form onSubmit={handleResults}>
        <Button children="+" onClick={addInput} className="m-5" />
        <Button children="Search" type="submit" />
        {inputs.map((input, index) => {
          return (<div key={index}>
            <SearchBox value={input} onChange={(e) => { handleSearchChange(index, e) }} />
            <Button children="-" onClick={() =>{removeInput(index)} } className="m-1 text-sm"  />
          </div>)
        })}
        </form>
      </div>
      <div style={{ maxWidth: "fit-content", padding: "50px", float: "left" }}>
        {results !== '' && displayInputs[0] !== '' ? (
          <>
            <p>You searched {
              displayInputs
            }
            </p>
          </>): ( results !== '' && <p>Please enter a keyword</p>)}
        <div> {results}</div>

      </div>

    </div>
  );
}
