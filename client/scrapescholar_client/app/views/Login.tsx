"use client";
import React, { useState, Dispatch, SetStateAction } from 'react';
import apiCalls from '../api/apiCalls';
import DOMPurify from 'dompurify';
interface LoginProps {
    setLoggedIn: Dispatch<SetStateAction<boolean>>;
    setToken: (item: string) => void;
}
const Login: React.FC<LoginProps> = ({ setLoggedIn, setToken }) => {
    const { postAPILogin } = apiCalls();

    const [username, setUserName] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [error, setError] = useState<string>('');
    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError('');
        const sanitizedUsername = DOMPurify.sanitize(username);
        const sanitizedPassword = DOMPurify.sanitize(password);
        const tokenResponse = await postAPILogin(sanitizedUsername, sanitizedPassword);
        if (tokenResponse && typeof tokenResponse === 'string') {
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
                            <input name="username_input" onChange={(event) => {
                                setUserName(event.target.value)
                            }}
                                value={username}
                                placeholder="Username" />
                        </label>
                    </div>
                    <div className="my-3">
                        <label>
                            <input name="password_input" type="password"
                                onChange={(event) => {
                                    setPassword(event.target.value)
                                }}
                                value={password}
                                placeholder="Password" />
                        </label>
                    </div>
                    <div className="flex justify-center">
                        <button name="login_button" type="submit" className={
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