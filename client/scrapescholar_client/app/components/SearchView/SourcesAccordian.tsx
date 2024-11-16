import React, { useState, useEffect } from 'react';
import apiCalls from '@/app/api/apiCalls';

interface SourcesAccordianProps {
    addToUserDatabaseList: (item: string) => void;
    removeFromUserDatabaseList: (item: string) => void;
}


const SourcesAccordian: React.FC<SourcesAccordianProps> = ({ addToUserDatabaseList, removeFromUserDatabaseList }) => {
    const { getAPIDatabases } = apiCalls();
    const [databases, setDatabases] = useState<string[]>([])
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
                        <span className="pl-3">Sources</span>
                    </button>
                </h2>
                <div className={openIndex === index ? '' : 'hidden'} id={`accordion-color-body-${index + 1}`}
                    aria-labelledby={`accordion-color-heading-${index + 1}`}>
                    <div className="pl-5 dark:border-gray-700">
                        {databases.map((database, index) => (
                            <div key={index + "check"}>
                                <label htmlFor={database}>
                                    <input id={database} type="checkbox"
                                        name={database} checked={checkboxes[database]}
                                        onChange={(event) => {
                                            handleCheckboxChange(event, database)
                                        }} />
                                    {database}
                                </label>
                            </div>))}
                    </div>
                </div>
            </div>
        </div>
    )
};

export default SourcesAccordian;
