import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
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

describe('SearchView US-8 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"

    test('US-8 Download button in response after search press', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        await waitFor(() => {
            expect(screen.getByText('Download')).toBeInTheDocument()
        }, { timeout: 5000 });
    })

    test('US-8 Download button is a link', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        await waitFor(() => {
            const downloadButton = screen.getByText('Download');
            expect(downloadButton).toHaveAttribute('href', '/csv');
        }, { timeout: 5000 });
    })

});
