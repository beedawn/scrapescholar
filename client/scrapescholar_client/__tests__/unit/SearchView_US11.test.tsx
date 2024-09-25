import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import '@testing-library/jest-dom';
import SearchView, { ResultItem } from '../../app/views/SearchView';
import React from 'react';
import Dropdown from '../../app/types/DropdownType';
import { sortResults } from '../../app/components/SearchView/ResultsTable';

import itemsArray from '../ItemsTestArray';
import itemsJson from '../ItemsTestJson';

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


  //US-11
  test('US-11 shows No results found after search press', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve(
          []
        ),
        headers: new Headers(),
        redirected: false,
        statusText: 'OK',
      })
    ) as jest.Mock;

    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('No Results Found')).toBeInTheDocument()
    }, { timeout: 5000 });
  })

  test('US-11 shows link in response after search press', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      expect(screen.getByText('link a')).toBeInTheDocument()
      expect(screen.getByText('link x')).toBeInTheDocument()
    }, { timeout: 5000 });
  })

});
