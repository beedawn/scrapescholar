"use client";
import React, { useState } from 'react';
import Head from 'next/head';
import SearchView from "./views/SearchView";
import Login from './views/Login';
export default function Home() {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);



  return (
    <div>

      {loggedIn ? (<SearchView setLoggedIn={setLoggedIn} />
      ) : (
        <>
          <Login setLoggedIn={setLoggedIn}/>
        </>
      )}

    </div>
  );
}
