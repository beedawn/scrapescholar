import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView, { ResultItem } from '../../app/views/SearchView';
import React from 'react';
import fetchMock from '../helperFunctions/apiMock';
import submitSearch from '../helperFunctions/submitSearch';


beforeEach(() => {
    global.fetch = fetchMock;
});
afterEach(() => {
    jest.restoreAllMocks();
});

describe('SearchView US-15 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"
    test('US-1 Search results should contain keyword', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput); 
        await waitFor(() => {
            const rows = screen.getAllByTestId('row')
            expect(within(rows[0]).queryByText(/test/)).toBeInTheDocument()
        },{timeout:5000})
        

    })

    

});
