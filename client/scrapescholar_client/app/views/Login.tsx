"use client";
import React, { useState, Dispatch, SetStateAction, } from 'react';
import SearchResults from "../components/SearchView/SearchResults";
import NavBar from "../components/SearchView/NavBar";
import Dropdown from "../types/DropdownType";

interface LoginProps {
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
   
}



const Login: React.FC<LoginProps> = ({ setLoggedIn}) => {
    
    return (
        <div className="flex flex-col sm:flex-row sm:mx-12 justify-center">
            <div className="flex-1 sm:mx-12 w-full">
            <button onClick={() => { setLoggedIn(true) }} className={"m-5 px-4 py-2 bg-blue-500 text-white rounded "}>
            Login
          </button>
            </div>
        </div>
    );
}
export default Login;