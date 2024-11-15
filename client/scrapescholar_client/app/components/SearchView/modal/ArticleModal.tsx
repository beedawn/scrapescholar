import React, { useState, useEffect } from 'react';
import Button from '../../Button';
import apiCalls from '@/app/api/apiCalls';
import DropdownSearchBox from '../../SearchView/DropdownSearchBox';
import DOMPurify from 'dompurify';
import { link } from 'fs';

enum DocumentType {
    Article,
    Document,
    Journal,
    Book
}

enum Source {
    None,

    Scopus=1,
    ScienceDirect=2,
    Other=3
}

interface AddArticleModalProps {
    addArticleView: () => void;
    search_id:number;
    handlePastSearchSelectionSearchID:
    (search_id:number) => void;
}

export interface NewArticle {
    search_id:number,
    title: string,
    date: string,
    citedby: string,
    source_id: number,
    document_type: string,
    abstract: string,
    link: string
}

interface DatabaseItem {
    name: string;
    source_id: number;
}


const { getAPIDatabasesAndIDs, addArticle } = apiCalls();

const AddArticleModal: React.FC<AddArticleModalProps> = ({ addArticleView, search_id, handlePastSearchSelectionSearchID }) => {
    const clearModal = () => {
        addArticleView();
    }
    const [databases, setDatabases] = useState<DatabaseItem[]>([])


    useEffect(() => {
        const fetchDatabases = async () => {
            const db_list = await getAPIDatabasesAndIDs();
            setDatabases(db_list);
        };
        fetchDatabases();
    }, []);


    const blankArticle:NewArticle = {
        search_id:search_id,
        title: "",
        date: "",
        citedby: "",
        document_type: "",
        source_id: 0,
        abstract:"",
        link:""
    }

    const [newArticle, setNewArticle] = useState<NewArticle>(blankArticle);
    const [error, setError] = useState<boolean>(false);


    const updateArticleState = (item: any, value: any) => {
        const sanitizedValue =  DOMPurify.sanitize(value);
        setNewArticle((prevState) => ({
            ...prevState,
            [item]: sanitizedValue
        }))
    }

    const submitArticle = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
       
        if (newArticle.title.length == 0 || newArticle.date.length == 0 || newArticle.citedby.length == 0 || newArticle.source_id ==0||newArticle.document_type.length == 0) {
            setError(true);
           
           
        } else {
            const dateArticle = {...newArticle, "date":new Date(parseInt(newArticle.date), 0, 1).toISOString().slice(0, 10), "citedby": parseInt(newArticle.citedby)}
            console.log(dateArticle)
            const response = await addArticle(dateArticle);
            // have articles reload?
            handlePastSearchSelectionSearchID(search_id)
            setNewArticle(blankArticle)
         
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
                newDocument = DocumentType.Document;
                break;
            case ("Book"):
                newDocument = DocumentType.Book;
                break;
            default:
                newDocument = DocumentType.Document;
        }
        updateArticleState("document_type", DocumentType[newDocument])
    }

    const dropdownSourceChange = (e: any) => {
        const selectedRole = e.target.value;
        for (let item of databases) {
            if (item.name == selectedRole) {
                updateArticleState("source_id", item.source_id)
                break;
            }
            else {
                updateArticleState("source_id", 3)
            }
        }
    }

    const [linkValidationError,setLinkValidationError]=useState<string>('');

    return (
        <div>

            <div className="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                <form onSubmit={(e) => { submitArticle(e) }}>
                    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                    <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                        <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                            <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl 
                            transition-all sm:my-8 sm:w-full sm:max-w-lg">
                                <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                                    <div className="flex items-start justify-between">
                                        <h3 className="text-base font-semibold text-gray-900" id="modal-title">New Article</h3>
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

                                <div className="bg-gray-50 px-2 py-1 flex  justify-center items-center text-black">
                                    <div>URL</div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <input className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Link" value={newArticle.link} onClick={() => {clearErrorSuccessMsg() }} onChange={(e) => {
                                                if(!e.target.value.startsWith("http://")&& !e.target.value.startsWith("https://")){
                                                    setLinkValidationError("Link must begin with http:// or https://")
                                                }
                                                else{
                                                    setLinkValidationError("")
                                                }
                                                updateArticleState("link", e.target.value)
                                            }}
                                            data-testid="new_article_link" />
                                           
                                    </div>
                                  
                                </div>
                                <div className="text-red-600 text-center">
                                            {linkValidationError.length>0?<>{linkValidationError}</>:<></>}
                                            </div>
                                <div className="flex gap-4 justify-center items-center text-center">
                                    <div className="flex flex-col items-center bg-gray-50 p-2">
                                        <label className="text-black mb-1">Year</label>
                                        <input
                                        type="number"
                                            className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Year"
                                            value={newArticle.date}
                                            onClick={() => { clearErrorSuccessMsg() }}
                                            onChange={(e) => { updateArticleState("date", e.target.value) }}
                                            data-testid="new_article_date"
                                        />
                                    </div>

                                    <div className="flex flex-col items-center bg-gray-50 p-2">
                                        <label className="text-black mb-1">Cited By</label>
                                        <input
                                        type="number"
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
                                            value={newArticle.abstract}
                                            onClick={() => { clearErrorSuccessMsg() }}
                                            onChange={(e) => { updateArticleState("abstract", e.target.value) }}
                                            data-testid="new_article_abstract"
                                        />
                                    </div>
                                </div>

                                <div className="bg-gray-50 px-4 py-3 flex justify-center items-center">
                                    <div>
                                        <DropdownSearchBox
                                            value={newArticle.document_type}
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
                                        <DropdownSearchBox value={Source[newArticle.source_id]} valueArray={databases.map((db) => db.name)} onDropdownChange={dropdownSourceChange} defaultValue="Source"
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
                                        <Button type="submit" onClick={() => {submitArticle }} data-testid="add_article_submit">Submit</Button>
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

export default AddArticleModal;