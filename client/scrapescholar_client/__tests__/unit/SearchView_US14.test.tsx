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

describe('SearchView US-14 Component', () => {
    const mockSetLoggedIn = jest.fn();
    const testInput = "test input"
    //UT-14.1
    test('US-14 article delete button should be in the document', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        await waitFor(() => {
            const deleteArticleButton = screen.getByTestId('delete_article_button')
            expect(deleteArticleButton).toBeInTheDocument();
        }, { timeout: 5000 });
    })
    //UT-14.2
    test('US-14 Add Document button should be in the document', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        await waitFor(() => {
            const addDocumentButton = screen.getByText("Add Document")
            expect(addDocumentButton).toBeInTheDocument()
        }, { timeout: 5000 });
    })
    //UT-14.3
    test('US-14 article delete button should be in the document, and prompt user before deletion', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        submitSearch(testInput);
        await waitFor(() => {
            const deleteArticleButton = screen.getByTestId('delete_article_button')
            fireEvent.click(deleteArticleButton)
            const deleteArticlePrompt = screen.getByTestId('delete_article_prompt')
            expect(deleteArticlePrompt).toBeInTheDocument()
        }, { timeout: 5000 });
    })


   
});
