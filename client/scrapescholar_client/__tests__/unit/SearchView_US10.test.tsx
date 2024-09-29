

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';

import fetchMock from '../helperFunctions/apiMock';

beforeEach(() => {
  global.fetch = fetchMock;
});

afterEach(() => {
  jest.restoreAllMocks();
});

describe('SearchView US-11 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"
    test('US-10 Sources should be displayed in UI', async () => {
        render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
        const searchButton = screen.getByText('Search');
        const inputs = screen.getAllByRole('textbox');
        fireEvent.change(inputs[0], { target: { value: testInput } });
        fireEvent.click(searchButton);

        await waitFor(() => {
            const rows = screen.getAllByTestId('row')
            expect(rows[0].children[6].textContent).toContain("Science Direct");
            expect(rows[1].children[6].textContent).toContain("Scopus");
        }, { timeout: 5000 });
    })
});



