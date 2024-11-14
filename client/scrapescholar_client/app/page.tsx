"use client";
import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import SearchView from "./views/SearchView";
import Login from './views/Login';
import apiCalls from './api/apiCalls';
import Loading from './components/Loading';
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
        {!loadingLogin?<Loading />:<>
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
