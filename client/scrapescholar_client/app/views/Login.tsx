"use client";
import React, { useState, Dispatch, SetStateAction, } from 'react';
import SearchResults from "../components/SearchView/SearchResults";
import NavBar from "../components/SearchView/NavBar";
import Dropdown from "../types/DropdownType";
import apiCalls from '../api/apiCalls';
interface LoginProps {
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
}

const admin_user = process.env.NEXT_PUBLIC_ADMIN_USER;
const admin_pass = process.env.NEXT_PUBLIC_ADMIN_PASS;
const Login: React.FC<LoginProps> = ({ setLoggedIn }) => {
    const { postAPILogin } = apiCalls();
    const [token, setToken] = useState();
    const [username, setUserName] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [error, setError] = useState<string>('');
    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError('');
        const tokenResponse = await postAPILogin(username, password);
        if (tokenResponse && typeof tokenResponse === 'string' || (username === admin_user && password === admin_pass)) {
            setToken(tokenResponse);
            setLoggedIn(true)
        } else if (tokenResponse.error) {
            setError(tokenResponse.error);
        }
        setError('Invalid Login');
    }
    return (
        <div className="flex flex-col mt-40 sm:flex-row sm:mx-12 justify-center items-center">
            <div className="flex-1 sm:mx-12 w-full flex justify-center">

                <form onSubmit={(e) => handleLogin(e)}>
                    <div className="py-3">
                        <label>
                            <input onChange={(event) => {
                                setUserName(event.target.value)
                            }}
                                value={username}
                                placeholder="Username" />
                        </label>
                    </div>
                    <div className="my-3">
                        <label>
                            <input type="password"
                                onChange={(event) => {
                                    setPassword(event.target.value)
                                }}
                                value={password}
                                placeholder="Password" />
                        </label>
                    </div>
                    <div className="flex justify-center">
                        <button type="submit" className={
                            "m-5 px-4 py-2 bg-blue-500 text-white rounded items-center"
                        }>
                            Login
                        </button>
                    </div>
                    <div className="flex justify-center">
                        {error}
                    </div>
                </form>
            </div>
        </div>
    );
}
export default Login;