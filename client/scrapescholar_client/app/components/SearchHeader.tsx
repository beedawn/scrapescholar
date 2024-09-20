import React from 'react';


import Button from './Button';
interface SearchHeaderProps {
downloadURL:string;
}
const SearchHeader: React.FC<SearchHeaderProps> = ({downloadURL}) => {
  

  
    return (
  

                    <div>
                        <div className="topContainer">
                            <div className="searchName">search name</div>
                           
                                <div className="downloadButton text-right">
                                     <Button>
                                        <a href={downloadURL}>Download</a> 
                                    </Button>   
                                </div>
                            
                        
                            </div>
                      
                    </div>
    )
};

export default SearchHeader;
