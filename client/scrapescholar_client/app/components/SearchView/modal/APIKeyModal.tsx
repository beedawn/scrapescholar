import React, { useState } from 'react';
import Button from '../../Button';
import apiCalls from '@/app/api/apiCalls';
import DOMPurify from 'dompurify';

interface APIKeyModalProps {
    setAPIKeyModalActive: (item: boolean) => void;
    setAPIKey: (item: APIKeyInterface) => void;
    APIKey:APIKeyInterface;
}
export interface APIKeyInterface {
    scopus: string,
    sciencedirect: string
}
const { verifyAPIKey } = apiCalls();
const APIKeyModal: React.FC<APIKeyModalProps> = ({ setAPIKeyModalActive, setAPIKey, APIKey }) => {
    const clearModal = () => {
        setAPIKeyModalActive(false);
    }

    const [result, setResult] = useState<boolean | null>(null);
    const [apiKeyInput, setAPIKeyInput] = useState<APIKeyInterface>({
        scopus: '',
        sciencedirect: ''
    });

    const handleAPIKeyInput = (value: string, field: string) => {
        if (value !==""){
        const newAPIKey = {
            ...APIKey,
            [field]: DOMPurify.sanitize(value)
        }
        setAPIKeyInput(newAPIKey)
    }
    }
    const handleSubmit = async () => {
        var keyNames = Object.keys(apiKeyInput) as Array<keyof APIKeyInterface>;
        for (let key of keyNames) {
            if (apiKeyInput[key] !== '') {
                const valid = await verifyAPIKey(apiKeyInput[key], key)
     
                if (!valid||valid==undefined) {
                    setResult(false)
                    return
                }
            }
        }
        setAPIKey(apiKeyInput)
        setAPIKeyModalActive(false)
    }

    return (
        <div>
            <div className="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                <form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
                    <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
                    <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
                        <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                            <div className="relative transform overflow-hidden rounded-lg bg-white text-left shadow-xl 
                        transition-all sm:my-8 sm:w-full sm:max-w-lg">
                                <div className="bg-white px-4 pb-4 pt-5 sm:p-6 sm:pb-4">
                                    <div className="flex items-start justify-between">
                                        <h3 className="text-base font-semibold text-gray-900" id="modal-title">API Keys</h3>
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

                                        </p>
                                    </div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                    <div>
                                        <input className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Scopus API Key" onClick={() => { setResult(null) }} onChange={(e) => { handleAPIKeyInput(e.target.value, 'scopus') }} data-testid="scopus-api-input"/>
                                    </div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                    <div>
                                        <input className="border rounded border-slate-800 text-center p-2"
                                            placeholder="Science Direct API Key" onClick={() => { setResult(null) }} onChange={(e) => { handleAPIKeyInput(e.target.value, 'sciencedirect') }} data-testid="sciencedirect-api-input" />
                                    </div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                    <div>
                                        {result == null ? <></> : result ? <div className="text-green-600">Success</div> : <div className="text-red-600" data-testid="api-failure">Failure</div>}
                                    </div>
                                </div>
                                <div className="bg-gray-50 px-4 py-3 flex  justify-center items-center">
                                    <div data-testid="api-key-submit">
                                        <Button type="submit" >Submit</Button>
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

export default APIKeyModal;




