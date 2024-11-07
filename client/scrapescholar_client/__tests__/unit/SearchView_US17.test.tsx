import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import apiCalls from '@/app/api/apiCalls';
import submitSearch from '../helperFunctions/submitSearch';
import itemsJson from '../mockData/ItemsTestJson';
import fetchMock, { setSimulateInsufficientStorage, setDeleteSearch } from '../helperFunctions/apiMock';

beforeEach(() => {
    global.fetch = fetchMock;
});

afterEach(() => {
    jest.restoreAllMocks();
});


describe('SearchView US-17 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"

//UT-25.1
    test('US-5 UT-5.1 check relevancy column contains %', () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} />);
        submitSearch(testInput)

        waitFor(() => {
            const rows = screen.getAllByTestId('row')
            expect(rows[0].children[9].textContent).toContain(/92/i);
            expect(rows[0].children[9].textContent).toContain(/%/i);
        }, { timeout: 5000 })
    });

    // test('US-17 Settings Accordion Expands and shows UserManagement for Admin', async () => {
    //     render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    //     const settingsAccordian = screen.getByText('Settings');
    //     fireEvent.click(settingsAccordian);
    //     await waitFor(() => {
    //         const userManagementLink = screen.getByText('User Management');
    //         const apiKeyLink = screen.getByText('API Keys');
    //         expect(userManagementLink).toBeInTheDocument();
    //         expect(apiKeyLink).toBeInTheDocument();
    //     }, { timeout: 5000 });

    // })

});
