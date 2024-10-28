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


//UT-25.1
describe('SearchView US-25 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"
    test('US-5 UT-5.1 check relevancy column contains %', () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} />);
        submitSearch(testInput)

        waitFor(() => {
            const rows = screen.getAllByTestId('row')
            expect(rows[0].children[9].textContent).toContain(/92/i);
            expect(rows[0].children[9].textContent).toContain(/%/i);
        }, { timeout: 5000 })
    });

});
