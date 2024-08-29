"use client";
import Image from "next/image";
import React, {useState} from 'react';
import Button from './components/Button';
import SearchBox from "./components/SearchBox";
export default function Home() {
  const [results, setResults]= useState('');
  const [inputs, setInputs]= useState(['']);
  const addInput = () =>{
      setInputs([...inputs,'']);
  }

  const handleSearchChange = (index:number, e: React.ChangeEvent<HTMLTextAreaElement>) => {
const newInputs = [...inputs];
 newInputs[index] =e.target.value;
 setInputs(newInputs);
  }

  const handleResults = () =>{

      setResults('No results found.')

  }
  return ( 
    <div style={{maxWidth:"fit-content", padding:"50px", marginLeft:"auto", marginRight:"auto"}}>
    {inputs.map((input, index) =>{
      return(<div  key={index}>
 <SearchBox value={input} onChange={(e)=>{handleSearchChange(index, e)}}/>
 
 </div>)
    })}
    <Button children="+" onClick={addInput} className="m-5"/>
    <Button children="Search" onClick={handleResults} />
    <div>
      {results}
      </div>
    </div>
  );
}
