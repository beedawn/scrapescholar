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
    //run off and get results somewhere
      setResults('No results found.')
  }
  return ( 
    <div>
    <div style={{maxWidth:"20%", padding:"50px", marginRight:"auto", float:"left"}}>
        <Button children="+" onClick={addInput} className="m-5"/>
        <Button children="Search" onClick={handleResults} />
    {inputs.map((input, index) =>{
      return(<div  key={index}>
 <SearchBox value={input} onChange={(e)=>{handleSearchChange(index, e)}}/>
 
 </div>)
    })}
 </div>
    <div style = {{maxWidth:"80%", padding:"50px", float:"left"}}>
      {results}
      </div>
   
    </div>
  );
}
