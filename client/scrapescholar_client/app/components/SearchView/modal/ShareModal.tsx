




import React, { useEffect } from 'react';

import SearchTitleField from './SearchTitleField';
import DOMPurify from 'dompurify';
import Button from '../../Button';

interface ShareModalProps {
    // downloadURL: string;
    // searchName: string;
    // setSearchName: (item: string) => void;
    // currentSearchId: number;
    // setLoading: (item: boolean) => void;
    setShareModalActive: (item: boolean) => void;
}
const ShareModal: React.FC<ShareModalProps> = ({ setShareModalActive }) => {
    const clearModal = () => {

        setShareModalActive(false);

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
                        <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg">
                            <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                                <div className="flex items-start justify-between">



                                    <h3 className="text-base font-semibold text-gray-900" id="modal-title">Share Search</h3>
                                    <div className="text-right"><button type="button" onClick={() => clearModal()} className="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:mt-0 sm:w-auto">Close</button>
                                    </div>
                                </div>

                                <div className="mt-2">
                                    <p className="text-sm text-gray-500 text-center">Please enter a username, or email address of the user you'd like to share your search with</p>
                                </div>
                            </div>
                            <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                <div><input className="border rounded border-slate-800 text-center p-2" placeholder="Username"></input></div>
                            </div>
                            <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                <div>
                                    <Button onClick={()=>clearModal()}>Submit</Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>





        </div>
    )
};

export default ShareModal;



