import React, { useState } from 'react';
import Button from '../Button';
import apiCalls from '@/app/api/apiCalls';

interface DataFullProps {
    searches: any[];
    setLoading: (item: boolean) => void;
}

const DataFull: React.FC<DataFullProps> =
    ({ searches, setLoading }) => {
        const [selectedValue, setSelectedValue] = useState<any[]>([]);
        const { deleteSearch } = apiCalls();
        const handleSelectChange = (event: any) => {
            const selectedOptions = Array.from(event.target.selectedOptions, option => (option as HTMLOptionElement).value);
            setSelectedValue(selectedOptions);
            console.log(selectedOptions)
        };
        const handleDeleteClick = async () => {
            setLoading(true)
            for (let item of selectedValue) {
                const numItem = Number(item)
                await deleteSearch(numItem)
            }
            setLoading(false)
        }
        return (
            <div className={"p-10"}>
                <p>SearchData is Full!</p>
                <p>
                    Please select some searches to
                    delete to perform additional searches:
                </p>
                <div className={"flex flex-wrap-reverse"}>
                    <div className={"float-left flex-none"}>
                        <select name="searches" id="searches" multiple style={{ color: "black" }} size={25} value={selectedValue} onChange={handleSelectChange}>
                            {searches.map((item, index) => (<option key={index} value={item.search_id} >{item.title}</option>))}
                        </select>
                    </div>
                    <div className={"float-right flex-1"}>
                        <Button className={"bg-red-600 m-5"} onClick={handleDeleteClick}>
                            Delete
                        </Button>
                    </div>
                </div>
            </div>)
    };

export default DataFull;
