import React from 'react';

interface AbstractModalProps {
    setAbstractText: (item: string) => void;
    text: string;
}

const AbstractModal: React.FC<AbstractModalProps> = ({ setAbstractText, text }) => {
    const clearModal = () => {
        setAbstractText('');
    }
    return (
        <div>
            <div className="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                    <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                        <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl 
                        transition-all sm:my-8 sm:w-full sm:max-w-lg">
                            <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                                <div className="flex items-start justify-between">
                                    <h3 className="text-base font-semibold text-gray-900" id="modal-title">Abstract</h3>
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
                                <div className="mt-2">
                                    <p className="text-sm text-gray-500 text-center">
                                        {text} </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default AbstractModal;




