"use client";
import Image from "next/image";
import React, { useState } from 'react';
import Button from './components/Button';
import SearchBox from "./components/SearchBox";
import LinePlot from "./components/d3/LinePlot";
export default function Home() {
  const [results, setResults] = useState('');
  const [inputs, setInputs] = useState(['']);
  const [displayInputs, setDisplayInputs] = useState<string[]>([]);
  const emptyString = '';

  const addInput = () => {
    setInputs([...inputs, emptyString]);
  }
  const removeInput = (index: number) => {
    const newInput = inputs.filter((_,input_index)=> input_index !== index)
    setInputs([...newInput]);
  }


  const handleSearchChange = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
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
      setInputs([emptyString])
    else
      setInputs([...filteredInputs])
  }
  return (
    <div>
      <div style={{ maxWidth: "400px", padding: "50px", marginRight: "auto", float: "left" }}>
        <h1 className="text-4xl font-bold">ScrapeScholar</h1>
        <form onSubmit={handleResults}>
        <Button onClick={addInput} className="m-5">+</Button>
        <Button type="submit" >Search</Button>
        {inputs.map((input, index) => {
          return (<div key={index}>
            <SearchBox value={input} onChange={(e) => { handleSearchChange(index, e) }} className="m-2 px-2 py-2 " />
            {index !=0 &&<Button onClick={() =>{removeInput(index)} } className="m-1 text-sm bg-red-600">-</Button>}
          </div>)
        })}
        </form>
      </div>
      <div style={{ maxWidth: "fit-content", padding: "50px", float: "left" }}>
        {results !== emptyString && displayInputs[0] !== emptyString ? (
          <>
            <p>You searched {
              displayInputs
            }
            </p>
          </>): ( results !== emptyString && <p className="bg-red-800 p-2 rounded">Please enter a keyword</p>)}
        <div> {results}</div>


        <div><LinePlot data={[20,40,50,60]} /></div>
      </div>
    </div>
  );
}
