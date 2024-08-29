"use client";
import Image from "next/image";
import React, {useState} from 'react';
import Button from './components/Button';
import SearchBox from "./components/SearchBox";
export default function Home() {
  const [text, setText]= useState('');
  const [inputs, setInputs]= useState(['']);
  const addInput = () =>{
    console.log("pizza");
    console.log(inputs);
      setInputs([...inputs,'']);
  }

  const handleSearchChange = (index:number, e: React.ChangeEvent<HTMLTextAreaElement>) => {
const newInputs = [...inputs];
 newInputs[index] =e.target.value;
 setInputs(newInputs);
console.log(inputs)
  }
  return ( 
    <>
    <p>hello world!</p>
    {inputs.map((input, index) =>{
      return(<div >
 <SearchBox key={index} value={input} onChange={(e)=>{handleSearchChange(index, e)}}/>
 
 </div>)
    })}
    <Button children="+" onClick={addInput}/>
    <Button children="Button" onClick={()=>(console.log(inputs))} />
    </>
  );
}
