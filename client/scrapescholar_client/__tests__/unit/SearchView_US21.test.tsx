import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import fetchMock300 from '../helperFunctions/apiMock300Searches';
import submitSearch from '../helperFunctions/submitSearch';
import apiCalls from '../../app/api/apiCalls';

beforeEach(() => {
    global.fetch = fetchMock300;
});

afterEach(() => {
    jest.restoreAllMocks();
});


// UT-24.1

describe('SearchView US-24 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"

    test('US-21 After 300 searches performed, prompt appears with delete button', async () => {
        
        act(()=>{render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);})
        await waitFor(() => {
            const selectElement = screen.getByRole('combobox')
            const deleteButton = screen.getByText('Delete');
            expect(selectElement).toBeInTheDocument();
            expect(deleteButton).toBeInTheDocument();
  
        }, { timeout: 5000 });
        
    })

    
  
 
});
