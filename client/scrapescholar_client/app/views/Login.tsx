"use client";
import React, { useState, Dispatch, SetStateAction, } from 'react';
import SearchResults from "../components/SearchView/SearchResults";
import NavBar from "../components/SearchView/NavBar";
import Dropdown from "../types/DropdownType";

interface LoginProps {
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
   
}

const admin_user = process.env.NEXT_PUBLIC_ADMIN_USER;
const admin_pass = process.env.NEXT_PUBLIC_ADMIN_PASS;

const Login: React.FC<LoginProps> = ({ setLoggedIn}) => {


    const loginPost = async(username:string, password:string) =>{
    const url = 'http://localhost:8000/auth/login';
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
try{
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData.toString()
    });
    if(!response.ok){
        const errorData = (response).json;
        throw new Error ('Network error:' +JSON.stringify(errorData))
    }
    const data = await response.json();
    return data.access_token;
}
catch(error){
    console.error('Error:', error);
    return null;
}
   

    }
    const [token, setToken]=useState();

    const [username, setUserName]=useState<string>('');
    const [password, setPassword]=useState<string>('');
    const [error, setError]=useState<string>('');
    const handleLogin = async(e: React.FormEvent<HTMLFormElement>)=>{

        e.preventDefault();
        setError('');
        const tokenResponse=await loginPost(username, password);
        
        if (tokenResponse){
            setToken(tokenResponse);
            setLoggedIn(true)
        }
      
        setError('Invalid Login');
        
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