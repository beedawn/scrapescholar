import React, { useState, useEffect } from 'react';
import Button from '../Button';
import apiCalls from '@/app/api/apiCalls';
import AddUserModal from './modal/AddUserModal';
import DeleteUserModal from './modal/DeleteUserModal';
import DropdownSearchBox from '../SearchView/DropdownSearchBox';
import Role from '@/app/types/Role';
interface UserManagementProps {
   
}

const UserManagement: React.FC<UserManagementProps> =
    ({  }) => {
        const [selectedValue, setSelectedValue] = useState<any[]>([]);
        const { deleteSearch, getUsers } = apiCalls();
        const [addUserModalActive, setAddUserModalActive]=useState(false);
        const [deleteUser, setDeleteUser]=useState();
        const [deleteUserModalActive, setDeleteUserModalActive]=useState(false);
        const getUsersAPI = async () =>{

            const user_list = await getUsers();
            setUsers(user_list)
            console.log(user_list)

        }
        useEffect(()=>{
        
            getUsersAPI()

        },[addUserModalActive, deleteUserModalActive])



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
            {deleteUserModalActive?<DeleteUserModal setDeleteUserModalActive={setDeleteUserModalActive} deleteUser={deleteUser}/>:<></>}
                {addUserModalActive?<>
                  
                <AddUserModal setAddUserModalActive={setAddUserModalActive}/>
                
                
                </>:<>
                
                <p>UserManagement</p>
                <p>
                    <Button onClick={()=>{setAddUserModalActive(true)}}>New User</Button>
             
                </p>
                <div className={"flex flex-wrap-reverse"}>
                    <div className={"m-5 float-left flex-none bg-white rounded text-black w-full"}>
               {users.map((user)=>(<div className="p-2 flex w-full" key={user.user_id}>
            
               <div className="p-2 w-1/4">{user.username}</div>
               <div className="w-1/4">
                                    <DropdownSearchBox value={Role[user.role_id]} valueArray={["Student","GradStudent","Professor"]} onDropdownChange={()=>{}} defaultValue="Role"/>
                                </div>



                                <div className="p-2 w-1/4">     
                <button className="bg-red-600 text-2xl p-1 rounded text-white" 
                onClick={()=>{setDeleteUserModalActive(true); setDeleteUser(user)}}>
                    ␡
                    </button>
               </div>

               <div className="p-2 w-1/4">     
                <Button className="" 
                onClick={()=>{setDeleteUserModalActive(true); setDeleteUser(user)}}>
                    Reset Password
                    </Button>
               </div>
               
               </div>))}
                    </div>
                 

               
                    {/* <div className={"float-right flex-1"}>
                    hi
                    </div> */}
                </div>
                
                
                </>}
                
            </div>)
    };

export default UserManagement;
