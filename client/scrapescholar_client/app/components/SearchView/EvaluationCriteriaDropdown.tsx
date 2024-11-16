import React, { useState, useEffect } from 'react';
import apiCalls from '@/app/api/apiCalls';
enum Evaluation {
    Accept,
    Pending,
    Reject,
}

interface EvaluationCriteriaDropdownProps {
    article_id: number;
    evaluationValue: string;
    disabled?: boolean;
}
const EvaluationCriteriaDropdown: React.FC<EvaluationCriteriaDropdownProps> = ({
    article_id,
    evaluationValue,
    disabled = false,
}) => {
    const [selected, setSelected] = useState({ value: "Evaluation", css: "bg-white-600" });
    const [isOpen, setIsOpen] = useState(false);
    const { putUserData } = apiCalls();

    useEffect(() => {
        if (evaluationValue == "Accept") handleChange(Evaluation.Accept, true);
        if (evaluationValue == "Pending") handleChange(Evaluation.Pending, true);
        if (evaluationValue == "Reject") handleChange(Evaluation.Reject, true);
    }, [evaluationValue]);

    const handleChange = async (input: Evaluation, init = false) => {
        let selectedValue = '';
        let cssStyling = '';

        switch (input) {
            case Evaluation.Reject:
                selectedValue = "Reject";
                cssStyling = "bg-red-600";
                break;
            case (Evaluation.Pending):
                selectedValue = "Pending";
                cssStyling = "bg-yellow-600";
                break;
            case (Evaluation.Accept):
                selectedValue = "Accept";
                cssStyling = "bg-green-600";
                break;
            default:
                break;

        }
        setSelected({ value: selectedValue, css: cssStyling });
        if (!init) {
            const putRequest = {
                article_id,
                evaluation_criteria: selectedValue,
            };
            await putUserData(putRequest);
        }
    };

    return (
        <div
            onClick={() => !disabled && setIsOpen(!isOpen)} // Only toggle if not disabled
            className={disabled ? "cursor-not-allowed opacity-50" : ""}
            data-testid={`evaluation-dropdown-${article_id}`}
        >
            {!isOpen && (
                <div className={`p-2 flex items-center ${selected.css}`}>
                    {selected.value}
                    <svg
                        className={`m-1 w-2 h-2 rotate-180`}
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 10 6"
                    >
                        <path
                            stroke="currentColor"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M9 5 5 1 1 5"
                        />
                    </svg>
                </div>
            )}
            <div>
                {isOpen && !disabled && (
                    <div className="p-3 bg-slate-800 text-white">
                        <div onClick={() => setIsOpen(false)}>× Close</div>
                        <div
                            className="p-2 bg-red-600"
                            onClick={() => handleChange(Evaluation.Reject)}
                        >
                            Reject
                        </div>
                        <div
                            className="bg-yellow-600 p-2"
                            onClick={() => handleChange(Evaluation.Pending)}
                        >
                            Pending
                        </div>
                        <div
                            className="bg-green-600 p-2"
                            onClick={() => handleChange(Evaluation.Accept)}
                        >
                            Accept
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EvaluationCriteriaDropdown;
