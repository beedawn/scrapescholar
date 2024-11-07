import React, { useState } from 'react';
import Button from '../../Button';
import apiCalls from '@/app/api/apiCalls';
import DropdownSearchBox from '../../SearchView/DropdownSearchBox';
import Role from '@/app/types/Role';
interface DeleteUserModalProps {
    setDeleteUserModalActive: (item: boolean) => void;
    deleteUser: any;
}

const { deleteUserAPI } = apiCalls();

const DeleteUserModal: React.FC<DeleteUserModalProps> = ({ setDeleteUserModalActive, deleteUser }) => {
    const clearModal = () => {
        setDeleteUserModalActive(false);
    }

    const submitDelete = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        await deleteUserAPI(deleteUser.user_id)
        clearModal()
    }

    return (
        <div>
            <div className="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                <form onSubmit={(e) => { submitDelete(e) }}>
                    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                    <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                        <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
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
                                    <div>
                                        <Button type="submit" className="bg-red-600" onClick={() => { }}>Delete</Button>   <Button className="bg-stone-500 border" onClick={() => { clearModal() }}>Cancel</Button>
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



