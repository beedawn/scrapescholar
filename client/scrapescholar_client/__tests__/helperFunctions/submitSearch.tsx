import {  screen, fireEvent, waitFor } from '@testing-library/react';
const submitSearch = (input:string) => {
    waitFor(()=>{

        const searchButton = screen.getByText('Search');
        const inputs = screen.getAllByRole('textbox');
        fireEvent.change(inputs[0], { target: { value: input } });
        fireEvent.click(searchButton);
    }, {timeout:5000})

  

    
}

export default submitSearch;