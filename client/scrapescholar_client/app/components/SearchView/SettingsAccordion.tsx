import React, { useState, useEffect } from 'react';
import apiCalls from '@/app/api/apiCalls';

interface SettingsAccordionProps {
    setOpenUserManagement: (item: boolean) => void;
    setDataFull: (item: boolean) => void;
    clearPages:()=>void;
}

const SettingsAccordian: React.FC<SettingsAccordionProps> = ({ setOpenUserManagement, setDataFull,clearPages }) => {
    const [isAdminUser, setIsAdminUser] = useState<boolean>(false);
    const { isAdmin } = apiCalls();
    useEffect(() => {
        const findAdmin = async () => {
            const result = await isAdmin()
            if (result === "true") {
                setIsAdminUser(true)
            }
        }
        findAdmin();
    }, [])

    const [hoveredClasses, setHoveredClasses] = useState<any>({ 1: "text-blue-400 underline", 2: "text-blue-400 underline" , 3:"text-blue-400 underline" });
    const updateHovered = (key: number) => {
        setHoveredClasses((prevState: any) => ({
            ...prevState,
            [key]: "text-blue-200 underline",
        }));
    }

    const removeHovered = (key: number) => {
        setHoveredClasses((prevState: any) => ({
            ...prevState,
            [key]: "text-blue-400 underline",
        }));
    }

    const [openIndex, setOpenIndex] = useState(null);
    const toggleAccordion = (index: any) => {
        setOpenIndex(openIndex === index ? null : index);
    };
    const index = 1;
    return (
        <div id="accordion-color">
            <div key={index}>
                <h2 id={`accordion-color-heading-${index + 1}`}>
                    <button
                        type="button"
                        className={`flex items-center 
                            w-full p-3 font-medium text-gray-500 
                                rounded-t-xl ${openIndex === index ? '' : ''}`}
                        onClick={() => toggleAccordion(index)}
                        aria-expanded={openIndex === index}
                        aria-controls={`accordion-color-body-${index + 1}`}
                        data-testid="user_settings"
                    >
                        <svg className={`w-3 h-3 ${openIndex === index ? 'rotate-180' : 'rotate-90'}`}
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"
                                strokeWidth="2" d="M9 5 5 1 1 5" />
                        </svg>
                        <span className="pl-3" >Settings</span>
                    </button>
                </h2>
                <div className={openIndex === index ? '' : 'hidden'} id={`accordion-color-body-${index + 1}`}
                    aria-labelledby={`accordion-color-heading-${index + 1}`}>
                    <div className="pl-5 dark:border-gray-700">
                        {isAdminUser ? <div key="1"  >
                            <a href="#" onClick={() => { clearPages();setOpenUserManagement(true); }}
                                onMouseEnter={() => { updateHovered(1) }}
                                onMouseLeave={() => { removeHovered(1) }}
                                className={hoveredClasses[1]}
                                data-testid="settings_user_management">
                                User Management
                            </a>
                        </div> : <></>}
                        <div key="2" onClick={() => alert("api keys")}  >
                            <a href="#" onMouseEnter={() => { updateHovered(2) }}
                                onMouseLeave={() => { removeHovered(2) }}
                                className={hoveredClasses[2]}>
                                API Keys
                            </a>
                        </div>
                        <div key="3" onClick={() => {clearPages();setDataFull(true)}}  >
                            <a href="#" onMouseEnter={() => { updateHovered(3) }}
                                onMouseLeave={() => { removeHovered(3) }}
                                className={hoveredClasses[3]}>
                                Article Management
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default SettingsAccordian;
