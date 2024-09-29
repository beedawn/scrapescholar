import {  screen, fireEvent } from '@testing-library/react';
const submitSearch = (input:string) => {
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: input } });
    fireEvent.click(searchButton);

    
}

export default submitSearch;