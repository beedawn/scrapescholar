import React, { useState, useEffect } from 'react';
import Button from '../Button';
import apiCalls from '@/app/api/apiCalls';
import AddUserModal from './modal/AddUserModal';

interface UserManagementProps {
   
}

const UserManagement: React.FC<UserManagementProps> =
    ({  }) => {
        const [selectedValue, setSelectedValue] = useState<any[]>([]);
        const { deleteSearch, getUsers } = apiCalls();
        const [addUserModalActive, setAddUserModalActive]=useState(false);

        const getUsersAPI = async () =>{

            const user_list = await getUsers();
            setUsers(user_list)
            console.log(user_list)

        }
        useEffect(()=>{
        
            getUsersAPI()

        },[addUserModalActive])

        const [users,setUsers]=useState<any[]>([]);
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
                {addUserModalActive?<>
                  
                <AddUserModal setAddUserModalActive={setAddUserModalActive}/>
                
                
                </>:<>
                
                <p>UserManagement</p>
                <p>
                    <Button onClick={()=>{setAddUserModalActive(true)}}>New User</Button>
             
                </p>
                <div className={"flex flex-wrap-reverse"}>
                    <div className={"float-left flex-none"}>
               {users.map((user)=>(<div key={user.user_id}>{user.username}</div>))}
                    </div>
                    <div className={"float-right flex-1"}>
                    hi
                    </div>
                </div>
                
                
                </>}
                
            </div>)
    };

export default UserManagement;
