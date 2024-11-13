import React, { useState, useEffect } from 'react';
import Button from '../../Button';
import apiCalls from '@/app/api/apiCalls';
import DropdownSearchBox from '../../SearchView/DropdownSearchBox';

import Role from '@/app/types/Role';

enum DocumentType {
    Article,
    Document,
    Journal,
    Book

}

enum Source {
    None,
    ScienceDirect,
    Scopus
}

interface AddUserModalProps {
    addArticleView: () => void;
}

export interface NewArticle {
    title: string,
    year: string,
    citedby: string,
    source_id: number,
    documenttype: string
}


// need to get list of sources either from navbar or just request again from backend for add article dropdown



const { getAPIDatabases } = apiCalls();
//need to get search id
const AddUserModal: React.FC<AddUserModalProps> = ({ addArticleView }) => {
    const clearModal = () => {
        addArticleView();
    }
    const [databases, setDatabases] = useState([])

    useEffect(() => {
        const fetchDatabases = async () => {
            const db_list = await getAPIDatabases();
            setDatabases(db_list);
            console.log(db_list)
        };
        fetchDatabases();
    }, []);
    

    const blankArticle = {
        title: "",
        year: "",
        citedby: "",
        documenttype:"",
        source_id:0
    }

    const [newArticle, setNewArticle] = useState<NewArticle>(blankArticle);
    const [error, setError] = useState<boolean>(false);


    const updateArticleState = (item: any, value: any) => {
        setNewArticle((prevState) => ({
            ...prevState,
            [item]: value
        }))
    }

    const submitArticle = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (newArticle.title.length == 0 || newArticle.year.length == 0 || newArticle.citedby.length == 0 || newArticle.role_id == 0 ) {
            setError(true);
        } else {
            // const response = await addArticle(newArticle);
            setNewArticle(blankArticle)
            // if (response === null) {
            //     setError(true)
            //     return
            // }
            clearModal()
        }
    }

    const clearErrorSuccessMsg = () => {
        setError(false);
    }

    const dropdownDocumentChange = (e: any) => {
        const selectedRole = e.target.value;
        let newDocument: DocumentType;
        switch (selectedRole) {
            case ("Article"):
                newDocument = DocumentType.Article;
                break;
            case ("Journal"):
                newDocument = DocumentType.Journal;
                break;
            case ("Document"):
                newDocument= DocumentType.Document;
                break;
            case ("Book"):
                newDocument= DocumentType.Book;
                break;
            default:
                newDocument = DocumentType.None;
        }

        console.log(newArticle);
        updateArticleState("documenttype", DocumentType[newDocument])
    }

    const dropdownSourceChange = (e: any) => {
        const selectedRole = e.target.value;
        let newSource: Source;
        switch (selectedRole) {
            case ("ScienceDirect"):
                newSource = Source.ScienceDirect;
                break;
            case ("Scopus"):
                newSource = Source.Scopus;
                break;
    
            default:
                newSource = Source.None;
        }
        updateArticleState("source_id", newSource)
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
                <form onSubmit={(e) => { submitArticle(e) }}>
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
                                    <div>Title</div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <input className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Title" value={newArticle.title} onClick={() => { clearErrorSuccessMsg() }} onChange={(e) => {
                                                updateArticleState("title", e.target.value)
                                            }}
                                            data-testid="new_article_title" />
                                    </div>
                                </div>
                                <div className="flex gap-4 justify-center items-center text-center">
                                    <div className="flex flex-col items-center bg-gray-50 p-2">
                                        <label className="text-black mb-1">Year</label>
                                        <input
                                            type="password"
                                            className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Year"
                                            value={newArticle.year}
                                            onClick={() => { clearErrorSuccessMsg() }}
                                            onChange={(e) => { updateArticleState("year", e.target.value) }}
                                            data-testid="new_article_year"
                                        />
                                    </div>

                                    <div className="flex flex-col items-center bg-gray-50 p-2">
                                        <label className="text-black mb-1">Cited By</label>
                                        <input
                                            className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Cited By"
                                            value={newArticle.citedby}
                                            onClick={() => { clearErrorSuccessMsg() }}
                                            onChange={(e) => { updateArticleState("citedby", e.target.value) }}
                                            data-testid="new_article_citedby"
                                        />
                                    </div>
                                </div>

                                <div className="bg-gray-50 px-2 py-1 flex  justify-center items-center text-black">
                                    <div>Abstract</div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <textarea
                                            className="border rounded border-slate-800 text-center text-black p-2 h-36  w-full resize-none"
                                            placeholder="Title"
                                            value={newArticle.title}
                                            onClick={() => { clearErrorSuccessMsg() }}
                                            onChange={(e) => { updateArticleState("title", e.target.value) }}
                                            data-testid="new_article_title"
                                        />
                                    </div>
                                </div>

                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <DropdownSearchBox
                                            value={newArticle.documenttype}
                                            valueArray={Object.keys(DocumentType)
                                                .filter((item) => {
                                                    return isNaN(Number(item));
                                                })}
                                            onDropdownChange={dropdownDocumentChange}
                                            defaultValue="Document Type"
                                            data-testid="new_article_document_type" />
                                    </div>
                                </div>

                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <DropdownSearchBox value={Source[newArticle.source_id]} valueArray={databases} onDropdownChange={dropdownSourceChange} defaultValue="Source"
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