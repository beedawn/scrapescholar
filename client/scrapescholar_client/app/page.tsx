"use client";
import React, { useState } from 'react';
import SearchView from "./views/SearchView";
export default function Home() {
const [loggedIn, setLoggedIn]=useState<boolean>(false);
  return (
    <div>
      {loggedIn?(<SearchView />
    ):(
    <><button onClick={()=>{setLoggedIn(true)}} className={"m-5 px-4 py-2 bg-blue-500 text-white rounded "}>Login</button></>
    )}
      
    </div>
  );
}
