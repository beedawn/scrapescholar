import React, { useState, useEffect } from 'react';
import apiCalls from '@/app/api/apiCalls';

interface SettingsAccordionProps {

    setOpenUserManagement:(item:boolean)=>void;
}

const SettingsAccordian: React.FC<SettingsAccordionProps> = ({ setOpenUserManagement }) => {
    const { getAPIDatabases, postAPILogin, getAPIResults } = apiCalls();
    const [databases, setDatabases] = useState([])
    useEffect(() => {
        const fetchDatabases = async () => {
            const db_list = await getAPIDatabases();
            setDatabases(db_list);
            // Initialize checkboxes with default checked state
            const initialCheckboxes = db_list.reduce(
                (accumulator: any[], db_source: any) => ({ ...accumulator, [db_source]: true }), {});
            setCheckboxes(initialCheckboxes);
        };
        fetchDatabases();
    }, []);
    const [hoveredClasses, setHoveredClasses]=useState<any>({1:"text-blue-400 underline",2:"text-blue-400 underline"});
    const updateHovered = (key:number) => {
        setHoveredClasses((prevState:any) => ({
            ...prevState,
            [key]: "text-blue-200 underline",
          }));  
      }
     
     const removeHovered = (key:number) => {
        setHoveredClasses((prevState:any) => ({
            ...prevState,
            [key]: "text-blue-400 underline",
          }));
     }

    const [openIndex, setOpenIndex] = useState(null);
    const [checkboxes, setCheckboxes] =
        useState<Record<string, boolean>>({});
    const toggleAccordion = (index: any) => {
        setOpenIndex(openIndex === index ? null : index);
    };

    const handleCheckboxChange = (
        event: React.ChangeEvent<HTMLInputElement>,
        database: string
    ) => {
        const checked = event.target.checked;
        setCheckboxes((prevState) => ({
            ...prevState,
            [database]: checked
        }))
        if (checked) {
            addToUserDatabaseList(database)
        } else {
            removeFromUserDatabaseList(database)
        }
    }
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
                    >
                        <svg className={`w-3 h-3 ${openIndex === index ? 'rotate-180' : 'rotate-90'}`}
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round"
                                strokeWidth="2" d="M9 5 5 1 1 5" />
                        </svg>
                        <span className="pl-3">Settings</span>
                    </button>
                </h2>
                <div className={openIndex === index ? '' : 'hidden'} id={`accordion-color-body-${index + 1}`}
                    aria-labelledby={`accordion-color-heading-${index + 1}`}>
                    <div className="pl-5 dark:border-gray-700">
                        
                            <div key="1"  >
                             
                                  <a href="#" onClick={()=>{setOpenUserManagement(true)}} onMouseEnter={()=>{updateHovered(1)}}  onMouseLeave={()=>{removeHovered(1)}} className={hoveredClasses[1]}>User Management</a>
                        
                            </div>
                            <div key="2" onClick={()=>alert("api keys")}  >
                               
                                   <a href="#" onMouseEnter={()=>{updateHovered(2)}}  onMouseLeave={()=>{removeHovered(2)}} className={hoveredClasses[2]}>API Keys</a>
                         
                            </div>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default SettingsAccordian;
