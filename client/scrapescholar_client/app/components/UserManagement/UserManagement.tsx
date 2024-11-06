import React, { useState } from 'react';
import Button from '../Button';
import apiCalls from '@/app/api/apiCalls';

interface UserManagementProps {
   
}

const UserManagement: React.FC<UserManagementProps> =
    ({  }) => {
        const [selectedValue, setSelectedValue] = useState<any[]>([]);
        const { deleteSearch } = apiCalls();
        // const handleSelectChange = (event: any) => {
        //     const selectedOptions = Array.from(event.target.selectedOptions, option => (option as HTMLOptionElement).value);
        //     setSelectedValue(selectedOptions);
        //     console.log(selectedOptions)
        // };
        // const handleDeleteClick = async () => {
        //     setLoading(true)
        //     for (let item of selectedValue) {
        //         const numItem = Number(item)
        //         await deleteSearch(numItem)
        //     }
        //     setLoading(false)
        // }
        return (
            <div className={"p-10"}>
                <p>UserManagement</p>
                <p>
             
                </p>
                <div className={"flex flex-wrap-reverse"}>
                    <div className={"float-left flex-none"}>
               
                    </div>
                    <div className={"float-right flex-1"}>
                    
                    </div>
                </div>
            </div>)
    };

export default UserManagement;
