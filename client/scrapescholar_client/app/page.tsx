"use client";
import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import SearchView from "./views/SearchView";
import Login from './views/Login';
import apiCalls from './api/apiCalls';
export default function Home() {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);
  const [token, setToken] = useState('');

  const [loadingLogin, setLoadingLogin]=useState(false);
  const {getCookie } = apiCalls();
  useEffect(() =>{
    const fetchCookie = async () =>
    {
      try{
    const cookie = await getCookie();
    if(cookie.detail=="Cookie not found" || cookie.detail=="Invalid token"){
        console.log("no cookie")
        setLoggedIn(false);
    }else{
        setToken(cookie.detail)
        setLoggedIn(true)
    }}
    catch(error){
      console.error("Error fetching cookie:", error);
    }
    finally{
      setLoadingLogin(true);
    }
    }
    fetchCookie();
    
},[])
  

  return (
    <div>
        {!loadingLogin?<>  <div className="flex flex-col mt-40 sm:flex-row sm:mx-12 justify-center items-center">
          <div className="flex-1 sm:mx-12 w-full flex justify-center">Loading</div></div></>:<>
          {loggedIn ? (<SearchView setLoggedIn={setLoggedIn} />
      ) : (
        <>
          <Login setLoggedIn={setLoggedIn} setToken={setToken}/>
        </>
      )}
        
        
        
        </>}
    

    </div>
  );
}
