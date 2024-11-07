import React, { useState } from 'react';
import Button from '../../Button';
import apiCalls from '@/app/api/apiCalls';
import DropdownSearchBox from '../../SearchView/DropdownSearchBox';
interface DeleteUserModalProps {
    setDeleteUserModalActive: (item: boolean) => void;
    deleteUser:any;
}

export interface NewUser {
    username: string,
    password: string,
    email: string,
    role_id: number
}

enum Role{
    Role,
    Professor,
    GradStudent,
    Student

}

const { addUser } = apiCalls();
//need to get search id
const DeleteUserModal: React.FC<DeleteUserModalProps> = ({ setDeleteUserModalActive,deleteUser }) => {
    const clearModal = () => {
        setDeleteUserModalActive(false);
    }
 
    const [result, setResult] = useState<boolean | null>(null);

    const [error, setError] = useState<boolean>(false);
   


    const submitDelete = async (e:React.FormEvent<HTMLFormElement>)=>{
        e.preventDefault();
   
    
            // await addUser()
    
            clearModal()
        
        
    }

    const clearErrorSuccessMsg = () =>{
        setError(false);

    }
    

    return (
        <div>

            <div className="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                {/* 
    Background backdrop, show/hide based on modal state.

    Entering: "ease-out duration-300"
      From: "opacity-0"
      To: "opacity-100"
    Leaving: "ease-in duration-200"
      From: "opacity-100"
      To: "opacity-0" */}
      <form onSubmit={(e)=>{submitDelete(e)}}>
                <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                    <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                        {/* Modal panel, show/hide based on modal state.

        Entering: "ease-out duration-300"
          From: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          To: "opacity-100 translate-y-0 sm:scale-100"
        Leaving: "ease-in duration-200"
          From: "opacity-100 translate-y-0 sm:scale-100"
          To: "opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
   */}
                        <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl 
                        transition-all sm:my-8 sm:w-full sm:max-w-lg">
                            <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                                <div className="flex items-start justify-between">
                                    <h3 className="text-base font-semibold text-gray-900" id="modal-title">Delete User</h3>
                                    <div className="text-right">
                                        <button type="button" onClick={() => clearModal()} className="mt-3 
                                        inline-flex w-full justify-center 
                                    rounded-md bg-white px-3 py-2 text-sm 
                                    font-semibold text-gray-900 shadow-sm ring-1 
                                    ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto">
                                            Close
                                        </button>
                                    </div>
                                </div>
                            </div>


                            <div className="bg-gray-50 px-2 py-1 flex  justify-center items-center text-black">
                                <div>Deleting this user is permanent.</div>
                            </div>
                            <div className="bg-gray-50 px-2 py-1 flex  justify-center items-center text-black">
                                <div>User: {deleteUser.username}</div>
                            </div>
                            
                            <div className="bg-gray-50 px-2 py-1 flex  justify-center items-center text-black">
                                <div> Please confirm to delete</div>
                            </div>
                          
                            <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                <div className="text-black">
                                    {error? <div className="text-red-600">Error, please try again.</div>:<></>}
                                </div>
                            </div>
                            <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                <div>
                                    <Button type="submit" className="bg-red-600" onClick={() => { }}>Delete</Button>   <Button className="bg-stone-500 border" onClick={() => { clearModal()}}>Cancel</Button>
                                </div>
                            </div>
                            <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                <div>
                                  
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </form>
            </div>





        </div>
    )
};

export default DeleteUserModal;




