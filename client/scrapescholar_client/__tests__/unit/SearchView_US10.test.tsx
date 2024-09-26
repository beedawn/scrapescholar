

import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView from '../../app/views/SearchView';
import React from 'react';
import itemsArray from '../ItemsTestArray';
import itemsJson from '../ItemsTestJson';
import { ResultItem } from '../../app/views/SearchView';

const items: ResultItem[] = itemsArray;

beforeEach(() => {
  // Reset mocks before each test
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      status: 200,
      json: () => Promise.resolve(itemsJson),
      headers: new Headers(),
      redirected: false,
      statusText: 'OK',

    })
  ) as jest.Mock;
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



