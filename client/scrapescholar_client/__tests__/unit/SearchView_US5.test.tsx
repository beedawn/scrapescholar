import { render, screen, fireEvent, waitFor, within, act } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';

import submitSearch from '../helperFunctions/submitSearch';
import itemsJson from '../mockData/ItemsTestJson';
import fetchMock, { setSimulateInsufficientStorage, setDeleteSearch } from '../helperFunctions/apiMock';

beforeEach(() => {
    global.fetch = fetchMock;
});

afterEach(() => {
    jest.restoreAllMocks();
});

describe('SearchView US-5 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"
    test('US-4 check relevancy column contains relevancy', () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} />);
        submitSearch(testInput)

waitFor(()=>{       
    const rows = screen.getAllByTestId('row')
    expect(rows[0].children[8].textContent).toContain(/Relevancy/i);
},{timeout:5000})
 

    });



   
});
