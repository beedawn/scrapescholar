import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import fetchMock from '../helperFunctions/apiMock';
import submitSearch from '../helperFunctions/submitSearch';


beforeEach(() => {
    global.fetch = fetchMock;
});

afterEach(() => {
    jest.restoreAllMocks();
});
// UT-24.1

describe('SearchView US-24 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"

    test('US-24 Frontend displays abstract', async () => {
        
        act(()=>{render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);})
        await waitFor(() => {
            const rows = screen.getAllByTestId('row')
            expect(rows[0].children[4].textContent).toContain("a");
            expect(rows[1].children[4].textContent).toContain("b");
        }, { timeout: 5000 });
        
    })


    // UT-24.3

    test('US-24 Frontend displays expand button in same cell as abstract', async () => {
        
        act(()=>{render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);})
        await waitFor(() => {
            const rows = screen.getAllByTestId('row')
            const expandButton = within(rows[0].children[4] as HTMLElement).getByRole('button', { name: /expand/i });
            const expandButton2 = within(rows[1].children[4] as HTMLElement).getByRole('button', { name: /expand/i });
            expect(expandButton).toBeInTheDocument()
            expect(expandButton2).toBeInTheDocument()
        }, { timeout: 5000 });
        
    })
 
});
