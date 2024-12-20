import React, { useState } from 'react';
import Button from '../../Button';
import apiCalls from '@/app/api/apiCalls';
import DropdownSearchBox from '../../SearchView/DropdownSearchBox';
import DOMPurify from 'dompurify';
import Role from '@/app/types/Role';
interface AddUserModalProps {
    setAddUserModalActive: (item: boolean) => void;
}

export interface NewUser {
    username: string,
    password: string,
    email: string,
    role_id: number
}

const { addUser } = apiCalls();

const AddUserModal: React.FC<AddUserModalProps> = ({ setAddUserModalActive }) => {
    const clearModal = () => {
        setAddUserModalActive(false);
    }

    const [newUser, setNewUser] = useState<NewUser>({
        username: "",
        password: "",
        email: "",
        role_id: 0
    });
    const [error, setError] = useState<boolean>(false);
    const updateUserState = (item: any, value: any) => {
        const sanitizedValue = DOMPurify.sanitize(value)
        setNewUser((prevState) => ({
            ...prevState,
            [item]: sanitizedValue
        }))
    }

    const submitUser = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (newUser.username.length == 0 || newUser.password.length == 0 || newUser.email.length == 0 || newUser.role_id == 0 || newUser.password.length < 8) {
            setError(true);
        } else {
            const response = await addUser(newUser);
            setNewUser({
                username: "",
                password: "",
                email: "",
                role_id: 0
            })
            if (response === null) {
                setError(true)
                return
            }
            clearModal()
        }
    }
    const clearErrorSuccessMsg = () => {
        setError(false);
    }

    const dropdownChange = (e: any) => {
        const selectedRole = e.target.value;
        let newRole: Role;
        switch (selectedRole) {
            case ("Professor"):
                newRole = Role.Professor;
                break;
            case ("GradStudent"):
                newRole = Role.GradStudent;
                break;
            case ("Student"):
                newRole = Role.Student;
                break;
            default:
                newRole = Role.Role;
        }
        updateUserState("role_id", newRole)
    }

    return (
        <div>

            <div className="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                <form onSubmit={(e) => { submitUser(e) }}>
                    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                    <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                        <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                            <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl 
                            transition-all sm:my-8 sm:w-full sm:max-w-lg">
                                <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                                    <div className="flex items-start justify-between">
                                        <h3 className="text-base font-semibold text-gray-900" id="modal-title">New User</h3>
                                        <div className="text-right">
                                            <button type="button" onClick={() => clearModal()} className="mt-3 
                                            inline-flex w-full justify-center 
                                            rounded-md bg-white px-3 py-2 text-sm 
                                            font-semibold text-gray-900 shadow-sm ring-1 
                                            ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto"
                                                data-testid="close_modal_button">
                                                Close
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                <div className="bg-gray-50 px-2 py-1 flex  justify-center items-center text-black">
                                    <div>Username</div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <input className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Username" value={newUser.username} onClick={() => { clearErrorSuccessMsg() }} onChange={(e) => { updateUserState("username", e.target.value) }}
                                            data-testid="new_user_username" />
                                    </div>
                                </div>

                                <div className="bg-gray-50 px-2 py-1 flex justify-center items-center text-black">
                                    <div>Password</div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <input type="password" className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Password" value={newUser.password} onClick={() => { clearErrorSuccessMsg() }} onChange={(e) => { updateUserState("password", e.target.value) }}
                                            data-testid="new_user_password" />
                                    </div>
                                </div>

                                <div className="bg-gray-50 px-2 py-1 flex justify-center items-center text-black">
                                    <div>Email</div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <input className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Email" value={newUser.email} onClick={() => { clearErrorSuccessMsg() }} onChange={(e) => { updateUserState("email", e.target.value) }}
                                            data-testid="new_user_email" />
                                    </div>
                                </div>

                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <DropdownSearchBox value={Role[newUser.role_id]} valueArray={["Student", "GradStudent", "Professor"]} onDropdownChange={dropdownChange} defaultValue="Role"
                                            data-testid="new_user_role" />
                                    </div>
                                </div>

                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div className="text-black">
                                        {error ? <div className="text-red-600">Error, please try again.</div> : <></>}
                                    </div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <Button type="submit" onClick={() => { }} data-testid="add_user_submit">Submit</Button>
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

export default AddUserModal;