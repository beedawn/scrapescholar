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

describe('SearchView US-4 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"
  test('US-4 check logout button renders in SearchView', () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} />);
    const logoutButton = screen.getByText('Logout');
    expect(logoutButton).toBeInTheDocument();
  });

  test('US-4 pencil is next to value in search title', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const searchTitleDiv = screen.getByTestId('search-title')
      console.log(searchTitleDiv)
      expect(searchTitleDiv.textContent).toContain("✎");
    }, { timeout: 5000 });
  })

  test('US-4 When user clicks on pencil next to search title, text field turns into input box', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const pencilIcons = screen.getAllByText("✎");
      fireEvent.click(pencilIcons[0]);
      const searchTitleDiv = screen.getByTestId('search-title')
      const input = searchTitleDiv.querySelector('input');
      expect(input).toBeInTheDocument();
    }, { timeout: 5000 });
  })

  test('US-4 When user clicks on pencil next to search title, text field turns into input box, then x button is pressed and reverts back to plain text', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const pencilIcons = screen.getAllByText("✎");
      fireEvent.click(pencilIcons[0]);
      const closeIcons = screen.getAllByText("×");
      fireEvent.click(closeIcons[0]);
      const searchTitleDiv = screen.getByTestId('search-title')
      const span = searchTitleDiv.querySelector('span');
      expect(span).toBeInTheDocument();
    }, { timeout: 5000 });
  })

  test('US-4 When user clicks on pencil next to search title, text field turns into input box, then check button is pressed and reverts back to new text', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let searchTitleDiv: Element | null = null;
    await waitFor(() => {
      const pencilIcons = screen.getAllByText("✎");
      fireEvent.click(pencilIcons[0]);
      searchTitleDiv = screen.getByTestId('search-title')
      const input = searchTitleDiv.querySelector('input');
      if (input) {
        fireEvent.change(input, { target: { value: testInput } });
        const checkIcons = screen.getAllByText("✔");
        fireEvent.click(checkIcons[0]);
      }
      else {
        fail('no input found after clicking pencil')
      }
    }, { timeout: 5000 });
    if (searchTitleDiv)
      expect(searchTitleDiv.textContent).toContain(testInput);
    else {
      fail('no input found after clicking pencil')
    }
  })
});
