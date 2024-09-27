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

describe('SearchView AR-4 Component', () => {
  const mockSetLoggedIn = jest.fn();
  const testInput = "test input"

  //AR-4
  test('AR-4 pencil is next to value in methodology', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    await waitFor(() => {
      const rows = screen.getAllByTestId('row')
      expect(rows[0].children[10].textContent).toContain("✎");
      expect(rows[1].children[10].textContent).toContain("✎");
    }, { timeout: 5000 });
  })

  test('AR-4 When user clicks on pencil next to value, text field turns into input box', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);

    await waitFor(() => {
      const pencilIcons = screen.getAllByText("✎");
      fireEvent.click(pencilIcons[0]);
      const rows = screen.getAllByTestId('row');
      const clarityField = rows[0].children[10];
      const input = clarityField.querySelector('input');
      expect(input).toBeInTheDocument();
    }, { timeout: 5000 });
  })

  test('AR-4 When user clicks on pencil next to value, text field turns into input box, then x button is pressed and reverts back to plain text', async () => {
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
      const rows = screen.getAllByTestId('row');
      const clarityField = rows[0].children[10];
      expect(clarityField.textContent).toContain("0");
    }, { timeout: 5000 });
  })

  test('AR-4 When user clicks on pencil next to value, text field turns into input box, then check button is pressed and reverts back to new text', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let clarityField: Element | null = null;
    await waitFor(() => {
      const pencilIcons = screen.getAllByText("✎");
      fireEvent.click(pencilIcons[1]);
      const rows = screen.getAllByTestId('row');
      clarityField = rows[0].children[10];
      const input = clarityField.querySelector('input');
      if (input) {
        fireEvent.change(input, { target: { value: testInput } });
        const checkIcons = screen.getAllByText("✔");
        fireEvent.click(checkIcons[0]);
      }
      else {
        fail('no input found after clicking pencil')
      }

    }, { timeout: 5000 });
    screen.debug(undefined,100000)
    if (clarityField)
      expect(clarityField.textContent).toContain(testInput);
    else {
      fail('no input found after clicking pencil')
    }
  })

  test('AR-4 When user clicks on pencil next to value, text field turns into input box, then check button is pressed and reverts back to new text', async () => {
    render(<SearchView setLoggedIn={mockSetLoggedIn} disableD3={true} />);
    const searchButton = screen.getByText('Search');
    const inputs = screen.getAllByRole('textbox');
    fireEvent.change(inputs[0], { target: { value: testInput } });
    fireEvent.click(searchButton);
    let clarityField: Element | null = null;
    let clarityField2: Element | null = null;
    let sortButton;
    await waitFor(() => {
      const transparencyScoreHeader = screen.getByText('Transparency');
      sortButton = within(transparencyScoreHeader.closest('th')).getByRole('button');
    }, { timeout: 5000 });
    if (sortButton) {
      fireEvent.click(sortButton);
    } else
      fail('no sort button found')
    await waitFor(() => {
      const pencilIcons = screen.getAllByText("✎");
      fireEvent.click(pencilIcons[1]);
      fireEvent.click(pencilIcons[5]);
      const rows = screen.getAllByTestId('row');
      clarityField = rows[0].children[10];
      const input = clarityField.querySelector('input');
      clarityField2 = rows[1].children[10];
      const input2 = clarityField2.querySelector('input');
      if (input && input2) {
        fireEvent.change(input, { target: { value: testInput + "1" } });
        fireEvent.change(input2, { target: { value: testInput + "2" } });
        const checkIcons = screen.getAllByText("✔");
        fireEvent.click(checkIcons[0]);
        fireEvent.click(checkIcons[1]);
      }
      else {
        fail('no input found after clicking pencil')
      }
    }, { timeout: 5000 });

    if (clarityField && clarityField2) {
      const rows = screen.getAllByTestId('row');
      expect(rows[0].children[10].textContent).toContain("test input1");
      expect(rows[1].children[10].textContent).toContain("test input2");
    }
    else {
      fail('no input found after clicking pencil')
    }
  })

});
