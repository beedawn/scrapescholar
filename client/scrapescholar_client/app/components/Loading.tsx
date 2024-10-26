import React from 'react';

const Loading =
    () => {
        return (
            <>
                <div className="flex flex-col mt-40 sm:flex-row sm:mx-12 justify-center items-center">
                    <div className="flex-1 sm:mx-12 w-full flex justify-center flex-col items-center">
                        <div>Loading</div>
                        <div>
                            <div className="lds-ring mt-2">
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                            </div></div>
                    </div>
                </div>
            </>
        )
    };

export default Loading;
