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



describe('SearchView US-5 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"
    test('US-5 UT-5.1 check relevancy column contains relevancy', () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} />);
        submitSearch(testInput)

        waitFor(() => {
            const rows = screen.getAllByTestId('row')
            expect(rows[0].children[8].textContent).toContain(/Relevancy/i);
        }, { timeout: 5000 })
    });
    test('US-5 UT-5.3 check relevancy column contains Relevant, SemiRelevant, and Not Relevant when expanded', () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} />);
        submitSearch(testInput)

        waitFor(() => {
            const rows = screen.getAllByTestId('row')
            const defaultRelevancyCell = within(rows[0]).getByTestId("relevancy-column-default")
            fireEvent.click(defaultRelevancyCell)
            expect(rows[0].children[8].textContent).toContain(/Relevant/i);
            expect(rows[0].children[8].textContent).toContain(/SemiRelevant/i);
            expect(rows[0].children[8].textContent).toContain(/Not Relevant/i);
        }, { timeout: 5000 })
    });
    test('US-5 UT-5.3 check relevancy column contains Relevant, SemiRelevant, and Not Relevant when expanded, and closes when close is pressed', () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} />);
        submitSearch(testInput)

        waitFor(() => {
            const rows = screen.getAllByTestId('row')
            const defaultRelevancyCell = within(rows[0]).getByTestId("relevancy-column-default")
            fireEvent.click(defaultRelevancyCell)
            expect(rows[0].children[8].textContent).toContain(/Relevant/i);
            expect(rows[0].children[8].textContent).toContain(/SemiRelevant/i);
            expect(rows[0].children[8].textContent).toContain(/Not Relevant/i);
        }, { timeout: 5000 })
        waitFor(() => {
            const closeRelevancy = screen.getByText(/Close/i)
            fireEvent.click(closeRelevancy)
        }, { timeout: 5000 })
        waitFor(() => {
        const rows = screen.getAllByTestId('row')
        expect(rows[0].children[8].textContent).not.toContain(/Relevant/i);
        expect(rows[0].children[8].textContent).not.toContain(/SemiRelevant/i);
        expect(rows[0].children[8].textContent).not.toContain(/Not Relevant/i);
        expect(rows[0].children[8].textContent).toContain(/Relevancy/i);
    }, { timeout: 5000 })
    });
    test('US-5 UT-5.1 check relevancy values can be clicked when expanded', () => {
        
        render(<SearchView setLoggedIn={mockSetLoggedIn} />);
        submitSearch(testInput)
        const { putUserData } = apiCalls();
        waitFor(() => {
            const rows = screen.getAllByTestId('row')
            const defaultRelevancyCell = within(rows[0]).getByTestId("relevancy-column-default")
            fireEvent.click(defaultRelevancyCell)
        }, { timeout: 5000 })

        waitFor(() => {
            const relevantItem = screen.getByText(/Relevant/i)
            fireEvent.click(relevantItem)
        }, { timeout: 5000 })
        waitFor(() => {
            const relevantItem = screen.getByText(/Relevant/i)
            expect(relevantItem).toBeInTheDocument()
            expect(screen.queryByText(/SemiRelevant/i)).not.toBeInTheDocument();
            expect(screen.queryByText(/Not Relevant/i)).not.toBeInTheDocument();
            expect(putUserData).toHaveBeenCalled();
        }, { timeout: 5000 })

    });


});
