"use client";
import React, { useState, Dispatch, SetStateAction, } from 'react';
import SearchResults from "../components/SearchView/SearchResults";
import NavBar from "../components/SearchView/NavBar";
import Dropdown from "../types/DropdownType";

interface LoginProps {
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
   
}



const Login: React.FC<LoginProps> = ({ setLoggedIn}) => {
    const [username, setUserName]=useState<string>('');
    const [password, setPassword]=useState<string>('');
    const [error, setError]=useState<string>('');
    const handleLogin = async(e)=>{
        e.preventDefault();
        setError('');
        if (username==="admin"&&password=="admin"){
            setLoggedIn(true)
        }
      
        setError('Invalid Login');
        //do something
    }
    return (
        <div className="flex flex-col mt-40 sm:flex-row sm:mx-12 justify-center items-center">
            <div className="flex-1 sm:mx-12 w-full flex justify-center">

                <form onSubmit={(e)=>handleLogin(e)}>
                    <div className="py-3"><label><input onChange={(event)=>{setUserName(event.target.value)}} value={username} placeholder="Username"></input></label></div>
                    <div className="my-3"><label><input type="password" onChange={(event)=>{setPassword(event.target.value)}} value={password} placeholder="Password"></input></label></div>
           <div className="flex justify-center"> <button type="submit" className={"m-5 px-4 py-2 bg-blue-500 text-white rounded items-center"}>
            Login
          </button>
      
          </div><div className="flex justify-center">{error}</div>
          </form>
            </div>
        </div>
    );
}
export default Login;