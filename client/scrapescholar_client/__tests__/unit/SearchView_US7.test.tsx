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


//UT-7.1
describe('SearchView US-7 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"
    test('US-5 UT-5.1 check relevancy column contains %', () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} />);
        submitSearch(testInput)
    let shareButton = null;
        waitFor(() => {
            shareButton = screen.getByText('Share');
            expect(shareButton).toBeInTheDocument();
            shareButton.click();
    
        }, { timeout: 5000 })
        waitFor(()=>{
            const submitButton = screen.getByText('Submit');
            const input = screen.getByPlaceholderText("Username");
            expect(submitButton).toBeInTheDocument();
            expect(input).toBeInTheDocument();
            const closeButton = screen.getByText("Close");
            expect(closeButton).toBeInTheDocument();
            closeButton.click()
        }, {timeout:5000})
        waitFor(()=>{
            const submitButton = screen.getByText('Submit');
            const input = screen.getByPlaceholderText("Username");
            expect(submitButton).not.toBeInTheDocument();
            expect(input).not.toBeInTheDocument();
            const closeButton = screen.getByText("Close");
            expect(closeButton).not.toBeInTheDocument();
        }, {timeout:5000})
    });

});
