import React, { useState } from 'react';
import Button from '../Button';

interface DataFullProps {
searches:any[];
}

const DataFull: React.FC<DataFullProps> =
    ({ searches}) => {
        const [selectedValue, setSelectedValue] = useState<any[]>([]);

        const handleSelectChange = (event:any) => {
            const selectedOptions = Array.from(event.target.selectedOptions, option => (option as HTMLOptionElement).value);
            setSelectedValue(selectedOptions); 
          console.log(selectedOptions)
        };
        const handleDeleteClick = ()=>{
            for(let item in selectedValue){
                    console.log(item)
            }
        }
      

        return (
            <div className={"p-10"}>
               <p>SearchData is Full!</p>
               <p>Please select some searches to delete to perform additional searches:</p><div className={"flex flex-wrap-reverse"}><div className={"float-left flex-none"}>
               <select name="searches" id="searches" multiple style={{color:"black"}} size={25} value={selectedValue} onChange={handleSelectChange}>
               {searches.map((item)=> (<option value={item.search_id} >{item.title}</option>))}
</select>
</div><div className={"float-right flex-1"}><Button className={"bg-red-600 m-5"} onClick={handleDeleteClick}>Delete </Button></div>

</div>
              
            </div>)
    };

export default DataFull;
