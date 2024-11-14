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
        const { deleteSearch, getUsers, updateUserRole } = apiCalls();
        const [addUserModalActive, setAddUserModalActive]=useState(false);
        const [deleteUser, setDeleteUser]=useState();
        const [deleteUserModalActive, setDeleteUserModalActive]=useState(false);
        const getUsersAPI = async () =>{

            const user_list = await getUsers();
            setUsers(user_list)

        }
        useEffect(()=>{
        
            getUsersAPI()

        },[addUserModalActive, deleteUserModalActive])

        // Handle role change
        const handleRoleChange = async (userId: number, newRole: string) => {
            await updateUserRole(userId, newRole);
            getUsersAPI(); // Refresh user list after update
        };

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
            <div className={"p-10"} data-testid="user_management">
            {deleteUserModalActive?<DeleteUserModal setDeleteUserModalActive={setDeleteUserModalActive} deleteUser={deleteUser}/>:<></>}
                {addUserModalActive?<>
                  
                <AddUserModal setAddUserModalActive={setAddUserModalActive}/>
                
                
                </>:<>
                
                <p>UserManagement</p>
                <p><Button onClick={()=>{setAddUserModalActive(true)}} data-testid="new_user_button">New User</Button></p>
                <div className={"flex flex-wrap-reverse"}>
                    <div className={"m-5 float-left flex-none bg-white rounded text-black w-full"}>
               {users.map((user)=>(<div className="p-2 flex w-full" key={user.user_id} data-testid="user_row">
            
               <div className="p-2 w-1/4" data-testid="user_username">{user.username}</div>
               <div className="w-1/4" data-testid="user_role">
               <DropdownSearchBox
                                            value={Role[user.role_id]}
                                            valueArray={["Student", "GradStudent", "Professor"]}
                                            onDropdownChange={(e) => handleRoleChange(user.user_id, e.target.value)}  // Call handleRoleChange
                                            defaultValue="Role"
                                            data-testid="role_dropdown"
                                        />
                                </div>



                <div className="p-2 w-1/4" data-testid="user_permissions">
                    <span data-testid="user_permissions_text"></span>  
                    <button className="bg-red-600 text-2xl p-1 rounded text-white" 
                    onClick={()=>{setDeleteUserModalActive(true); setDeleteUser(user)}} data-testid="delete_user_button">
                        ␡
                        </button>
               </div>

               <div className="p-2 w-1/4">     
                <Button className="" 
                onClick={()=>{}}
                data-testid="reset_password_button">
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
